import logging
from datetime import datetime

from pyspark.sql.functions import round, col, avg, stddev, when, from_json, window, year, month, dayofmonth
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, LongType, DoubleType

from metrics_type import MetricsType

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


class MetricsTypeMemory(MetricsType):
    def __init__(self, window_size, window_slide, threshold):
        self.window_size = window_size
        self.window_slide = window_slide
        self.threshold = threshold

    def process_stream(self, df):
        """ Create a Spark Streaming DataFrame that connects to a Kafka """
        # Define the Kafka topic schema
        schema_mem = StructType([
            StructField("name", StringType()),
            StructField("timestamp", TimestampType()),
            StructField("fields",
                        StructType([
                            StructField("available", LongType()),
                            StructField("free", LongType()),
                            StructField("total", LongType()),
                            StructField("used_percent", DoubleType())
                        ])
                        ),
            StructField("tags",
                        StructType([
                            StructField("host", StringType())
                        ])
                        )
        ])

        parsed_df = df.selectExpr("CAST(value AS STRING)") \
            .select(from_json("value", schema_mem).alias("data")) \
            .select("data.timestamp", "data.tags.host", "data.name",
                    round("data.fields.used_percent", 2).alias("used_percent")) \
            .withWatermark("timestamp", "30 seconds")

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
        updated_stream = stream \
            .select("*", window(col("timestamp"), f"{self.window_size} seconds", f"{self.window_slide} seconds").alias(
            "window")) \
            .filter(col("host") == "k8s-worker-1") \
            .withWatermark("timestamp", "30 seconds")
        # .withcolumn("window", window(col("timestamp"), f"{window_size} seconds", f"{window_slide} seconds"))

        updated_stream.join(windowed_stream, on=((updated_stream["window"] == windowed_stream["window"]) & (
                    updated_stream["host"] == windowed_stream["host"])), how="full")

        stream_with_window = updated_stream \
            .join(windowed_stream, on=(["window", "host"]), how="full") \
            .withWatermark("timestamp", "30 seconds")

        logging.info(f'updated_stream DF ->')
        updated_stream.printSchema()

        logging.info(f'stream_with_window DF ->')
        stream_with_window.printSchema()

        anomaly_df = windowed_stream.withColumn("is_anomaly", when(
            (col("avg") < 10) | (col("avg") > 80), 1).otherwise(0))

        return updated_stream
