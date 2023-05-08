import logging
import os
import sys

from multiprocessing import Process

from disk_metrics import MetricsTypeDisk
from memory_metrics import MetricsTypeMemory

from pyspark.sql import SparkSession

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get the Elasticsearch, Kafka broker, and topic
# kafka_broker = os.environ['KAFKA_BROKER']
# kafka_topic = os.environ['KAFKA_TOPIC']
# es_nodes = os.environ['ES_NODES']
kafka_broker = "bitnami-kafka-headless.observability.svc.cluster.local:9092"
# kafka_topic = "telegraf_disk"
es_nodes = "elasticsearch-master.observability.svc.cluster.local:9200"
window_size, window_slide, threshold = 30, 10, 2


# Define the schema for the incoming Kafka data
# schema = StructType([
#     StructField("name", StringType()),
#     StructField("timestamp", TimestampType()),
#     StructField("fields",
#                 StructType([
#                     StructField("free", LongType()),
#                     StructField("total", LongType()),
#                     StructField("used", LongType()),
#                     StructField("used_percent", DoubleType())
#                 ])
#                 ),
#     StructField("tags",
#                 StructType([
#                     StructField("device", StringType()),
#                     StructField("fstype", StringType()),
#                     StructField("host", StringType()),
#                     StructField("mode", StringType()),
#                     StructField("path", StringType())
#                 ])
#                 )
# ])


# Define the anomaly detection function
# def detect_anomalies(stream, window_size=30, threshold=2):
#     """
#     Args:
#         stream: A streaming DataFrame.
#         window_size: The size of the window in seconds.
#         threshold: The threshold for anomaly detection.
#
#     Returns:
#         A streaming DataFrame with an additional column for each column in the original DataFrame, indicating whether
#         the value is an anomaly or not.
#     """
#     window_slide = 10
#     logging.info('In detect_anomalies...')
#
#     # Calculate the standard deviation of each column over a window of specified size
#     windowed_stream = stream \
#         .withWatermark("timestamp", "30 seconds") \
#         .groupBy(window(col("timestamp"), f"{window_size} seconds", f"{window_slide} seconds"), col("host")) \
#         .agg(avg("used_percent").alias("avg"), stddev("used_percent").alias("std")) \
#         .select("window", "host", round('avg', 2).alias("avg"), round("std", 2).alias("std")) \
#         .filter(col("host") == "k8s-worker-1")
#
#     # Calculate the upper and lower bounds for anomaly detection
#     windowed_stream = windowed_stream.withColumn("lower_bound", col("avg") - threshold * col("std"))
#     windowed_stream = windowed_stream.withColumn("upper_bound", col("avg") + threshold * col("std"))
#
#     logging.info(f'windowed_stream DF ->')
#     windowed_stream.printSchema()
#
#     # Join the lower and upper bounds with the original stream to detect anomalies
#     # join_condition = "lower_bound_stream.time_window = upper_bound_stream.time_window"
#     updated_stream = stream \
#         .select("*", window(col("timestamp"), f"{window_size} seconds", f"{window_slide} seconds").alias("window")) \
#         .filter(col("host") == "k8s-worker-1") \
#         .withWatermark("timestamp", "30 seconds")
#     # .withcolumn("window", window(col("timestamp"), f"{window_size} seconds", f"{window_slide} seconds"))
#
#     #updated_stream = updated_stream.withWatermark("timestamp", "30 seconds")
#
#     updated_stream.join(windowed_stream, on=((updated_stream["window"] == windowed_stream["window"]) & (updated_stream["host"] == windowed_stream["host"])), how="full")
#
#     stream_with_window = updated_stream \
#         .join(windowed_stream, on=(["window", "host"]), how="full") \
#         .withWatermark("timestamp", "30 seconds")
#     # stream_with_window = updated_stream \
#     #     .join(windowed_stream, on=(["window", "host"]), how="full") \
#     #     .withWatermark("timestamp", "30 seconds")
#
#     logging.info(f'updated_stream DF ->')
#     updated_stream.printSchema()
#
#     logging.info(f'stream_with_window DF ->')
#     stream_with_window.printSchema()
#
#     anomaly_df = windowed_stream.withColumn("is_anomaly", when(
#         (col("avg") < 10) | (col("avg") > 80), 1).otherwise(0))
#
#     # # Add a new column for each column in the original stream, indicating whether the value is an anomaly or not
#     # anomaly_df = stream_with_window.withColumn("is_anomaly", when(
#     #     (stream_with_window.used_percent < stream_with_window.lower_bound) | (
#     #                 stream_with_window.used_percent > stream_with_window.upper_bound), 1).otherwise(0))
#     # # for column in stream.columns:
#     # #      anomaly_column = f"anomaly_{column}"
#     # #      anomaly_stream = anomaly_stream.withColumn(anomaly_column, when(
#     # #          col(column) < col("lower_bound") | col(column) > col("upper_bound"), 1).otherwise(0))
#     #
#     # final_df = anomaly_df \
#     #     .groupBy(col("window"), col("host")) \
#     #     .agg(count("is_anomaly").alias("count"))  # \
#     # # .select("window", "host", round('avg', 2).alias("avg"), round("std", 2).alias("std"))
#
#     return updated_stream


def start_process(topic, spark):
    # """ Create a Spark Streaming DataFrame that connects to a Kafka """
    # # Define the Kafka source and read data as a DataFrame
    # df = spark \
    #     .readStream \
    #     .format("kafka") \
    #     .option("kafka.bootstrap.servers", kafka_broker) \
    #     .option("subscribe", topic) \
    #     .option("startingOffsets", "latest") \
    #     .load()
    #
    # logging.info(f'Original DF ->')
    # df.printSchema()
    #
    # parsed_df = df.selectExpr("CAST(value AS STRING)") \
    #     .select(from_json("value", schema).alias("data")) \
    #     .select("data.timestamp", "data.tags.host", "data.name", round("data.fields.used_percent", 2).alias("used_percent")) \
    #     .withWatermark("timestamp", "30 seconds")
    # #    .select("data.*")
    #
    # logging.info(f'parsed_df DF ->')
    # parsed_df.printSchema()
    #
    # file_name = "/tmp/metrics"
    #
    # formatted_df = parsed_df \
    #     .withColumn("year", year("timestamp")) \
    #     .withColumn("month", month("timestamp")) \
    #     .withColumn("day", dayofmonth("timestamp")) \
    #     .writeStream \
    #     .trigger(processingTime='30 seconds') \
    #     .outputMode("append") \
    #     .format("csv") \
    #     .option("header", "true") \
    #     .option("path", file_name) \
    #     .option("checkpointLocation", "/tmp/checkpoint/dir") \
    #     .partitionBy("name", "year", "month", "day") \
    #     .option("truncate", "false") \
    #     .start()
    #
    # # Call the detect_anomalies function to add anomaly columns to the stream
    # anomaly_stream = detect_anomalies(parsed_df, window_size=30, threshold=2)
    #
    # # .withWatermark("timestamp", "30 seconds") \
    # query = anomaly_stream \
    #     .writeStream \
    #     .trigger(processingTime='30 seconds') \
    #     .outputMode("Append") \
    #     .format("console") \
    #     .option("truncate", "false") \
    #     .option("numRows", 50) \
    #     .start()
    #
    # logging.info(f'Current time is {datetime.now()}')
    #
    # query.awaitTermination()
    # formatted_df.awaitTermination()
    logging.info(f'Topic is {topic}.')
    if topic == 'telegraf_disk':
        # Define the Kafka source and read data as a DataFrame
        df_disk = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_broker) \
            .option("subscribe", topic) \
            .option("startingOffsets", "latest") \
            .load()

        logging.info(f'Original DF ->')
        #df.printSchema()

        disk = MetricsTypeDisk(window_size, window_slide, threshold)
        disk.process_stream(df=df_disk)
    elif topic == 'telegraf_mem':
        # Define the Kafka source and read data as a DataFrame
        df_mem = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_broker) \
            .option("subscribe", topic) \
            .option("startingOffsets", "latest") \
            .load()

        logging.info(f'Original DF ->')
        #df.printSchema()

        memory = MetricsTypeMemory(window_size, window_slide, threshold)
        memory.process_stream(df=df_mem)
    else:
        logging.error(f'Unknown topic {topic}. Exiting thread for this topic.')
        sys.exit(1)


def main():
    """Main function"""
    try:
        threads = []
        topics = ['telegraf_disk', 'telegraf_mem', 'telegraf_cpu', 'telegraf_net']
        # topics = ['telegraf_disk', 'telegraf_mem']

        logging.info(f'Number of Kafka topic to start reading data: {len(topics)}.')

        # Create a SparkSession
        spark = SparkSession \
            .builder \
            .appName("MetricsStream") \
            .config("spark.sql.streaming.statefulOperator.checkCorrectness.enabled", "false") \
            .getOrCreate()

        spark.sparkContext.setLogLevel("WARN")

        for topic in topics:
            thread = Process(target=start_process, args=(topic, spark,))
            threads.append(thread)
            thread.start()

        # wait for the threads to complete
        for t in threads:
            t.join()
    except Exception as e:
        logging.error("Unable to start thread", exc_info=True)

    # Start the Spark session
    spark.streams.awaitAnyTermination()


if __name__ == '__main__':
    main()
