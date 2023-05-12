import logging
import sys
from datetime import datetime

from metrics_type import MetricsType

from pyspark.sql.functions import round, split, col, count, avg, stddev, when, from_json, window, year, month, \
    dayofmonth
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, ArrayType, LongType, DoubleType

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


class MetricsTypeDisk(MetricsType):
    def __init__(self, window_size, window_slide, threshold):
        self.window_size = window_size
        self.window_slide = window_slide
        self.threshold = threshold

    def process_stream(self, df):
        """ Create a Spark Streaming DataFrame that connects to a Kafka """
        # Define the Kafka topic schema
        schema_disk = StructType([
            StructField("name", StringType()),
            StructField("timestamp", TimestampType()),
            StructField("fields",
                        StructType([
                            StructField("free", LongType()),
                            StructField("total", LongType()),
                            StructField("used", LongType()),
                            StructField("used_percent", DoubleType())
                        ])
                        ),
            StructField("tags",
                        StructType([
                            StructField("device", StringType()),
                            StructField("fstype", StringType()),
                            StructField("host", StringType()),
                            StructField("mode", StringType()),
                            StructField("path", StringType())
                        ])
                        )
        ])

        # convert the message value from a JSON string to a DataFrame
        # df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)").toDF("key", "value")
        # parsed_df = df.selectExpr("CAST(value AS STRING)") \
        #    .select(split("value", " ").alias("data")) \
        #    .selectExpr("data[0] as plugin_tags", "data[1] as metrics", "data[2] as measurement_ts")

        parsed_df = df.selectExpr("CAST(value AS STRING)") \
            .select(from_json("value", schema_disk).alias("data")) \
            .select("data.timestamp", "data.tags.host", "data.name",
                    round("data.fields.used_percent", 2).alias("used_percent")) \
            .withWatermark("timestamp", "30 seconds")
        #    .select("data.*")

        logging.info(f'parsed_df DF ->')
        parsed_df.printSchema()

        file_name = "/tmp/metrics"

        formatted_df = parsed_df \
            .withColumn("year", year("timestamp")) \
            .withColumn("month", month("timestamp")) \
            .withColumn("day", dayofmonth("timestamp")) \
            .writeStream \
            .trigger(processingTime='30 seconds') \
            .outputMode("append") \
            .format("csv") \
            .option("header", "true") \
            .option("path", file_name) \
            .option("checkpointLocation", "/tmp/checkpoint/dir") \
            .partitionBy("name", "year", "month", "day") \
            .option("truncate", "false") \
            .start()

        # Call the detect_anomalies function to add anomaly columns to the stream
        anomaly_stream = self.detect_anomalies(parsed_df)

        # .withWatermark("timestamp", "30 seconds") \
        query = anomaly_stream \
            .writeStream \
            .trigger(processingTime='30 seconds') \
            .outputMode("Append") \
            .format("console") \
            .option("truncate", "false") \
            .option("numRows", 50) \
            .start()

        logging.info(f'Current time is {datetime.now()}')

        query.awaitTermination()
        formatted_df.awaitTermination()

    def detect_anomalies(self, stream):
        """
        Args:
            stream: A streaming DataFrame.
            window_size: The size of the window in seconds.
            threshold: The threshold for anomaly detection.

        Returns:
            A streaming DataFrame with an additional column for each column in the original DataFrame, indicating whether
            the value is an anomaly or not.
        """
        # window_slide = 10
        logging.info('In detect_anomalies...')

        # Calculate the standard deviation of each column over a window of specified size
        windowed_stream = stream \
            .withWatermark("timestamp", "30 seconds") \
            .groupBy(window(col("timestamp"), f"{self.window_size} seconds", f"{self.window_slide} seconds"),
                     col("host")) \
            .agg(avg("used_percent").alias("avg"), stddev("used_percent").alias("std")) \
            .select("window", "host", round('avg', 2).alias("avg"), round("std", 2).alias("std")) \
            .filter(col("host") == "k8s-worker-1")

        # Calculate the upper and lower bounds for anomaly detection
        windowed_stream = windowed_stream.withColumn("lower_bound", col("avg") - self.threshold * col("std"))
        windowed_stream = windowed_stream.withColumn("upper_bound", col("avg") + self.threshold * col("std"))

        logging.info(f'windowed_stream DF ->')
        windowed_stream.printSchema()

        # Join the lower and upper bounds with the original stream to detect anomalies
        # join_condition = "lower_bound_stream.time_window = upper_bound_stream.time_window"
        updated_stream = stream \
            .select("*", window(col("timestamp"), f"{self.window_size} seconds", f"{self.window_slide} seconds").alias(
            "window")) \
            .filter(col("host") == "k8s-worker-1") \
            .withWatermark("timestamp", "30 seconds")
        # .withcolumn("window", window(col("timestamp"), f"{window_size} seconds", f"{window_slide} seconds"))

        # updated_stream = updated_stream.withWatermark("timestamp", "30 seconds")

        updated_stream.join(windowed_stream, on=((updated_stream["window"] == windowed_stream["window"]) & (
                    updated_stream["host"] == windowed_stream["host"])), how="full")

        stream_with_window = updated_stream \
            .join(windowed_stream, on=(["window", "host"]), how="full") \
            .withWatermark("timestamp", "30 seconds")
        # stream_with_window = updated_stream \
        #     .join(windowed_stream, on=(["window", "host"]), how="full") \
        #     .withWatermark("timestamp", "30 seconds")

        logging.info(f'updated_stream DF ->')
        updated_stream.printSchema()

        logging.info(f'stream_with_window DF ->')
        stream_with_window.printSchema()

        anomaly_df = windowed_stream.withColumn("is_anomaly", when(
            (col("avg") < 10) | (col("avg") > 80), 1).otherwise(0))

        # # Add a new column for each column in the original stream, indicating whether the value is an anomaly or not
        # anomaly_df = stream_with_window.withColumn("is_anomaly", when(
        #     (stream_with_window.used_percent < stream_with_window.lower_bound) | (
        #                 stream_with_window.used_percent > stream_with_window.upper_bound), 1).otherwise(0))
        # # for column in stream.columns:
        # #      anomaly_column = f"anomaly_{column}"
        # #      anomaly_stream = anomaly_stream.withColumn(anomaly_column, when(
        # #          col(column) < col("lower_bound") | col(column) > col("upper_bound"), 1).otherwise(0))
        #
        # final_df = anomaly_df \
        #     .groupBy(col("window"), col("host")) \
        #     .agg(count("is_anomaly").alias("count"))  # \
        # # .select("window", "host", round('avg', 2).alias("avg"), round("std", 2).alias("std"))

        return updated_stream
