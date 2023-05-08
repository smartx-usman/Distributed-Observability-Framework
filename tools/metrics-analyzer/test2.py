import logging
import os
import sys

from multiprocessing import Process

from pyspark.sql.functions import round, col, avg, stddev, when, from_json, window, year, month, dayofmonth
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, LongType, DoubleType

# from disk_metrics import MetricsTypeDisk
# from memory_metrics import MetricsTypeMemory

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

schema_net = StructType([
    StructField("name", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("fields",
                StructType([
                    StructField("bytes_recv", LongType()),
                    StructField("bytes_sent", LongType()),
                    StructField("drop_in", LongType()),
                    StructField("drop_out", LongType()),
                    StructField("err_in", LongType()),
                    StructField("err_out", LongType()),
                    StructField("packets_recv", LongType()),
                    StructField("packets_sent", LongType())
                ])
                ),
    StructField("tags",
                StructType([
                    StructField("host", StringType()),
                    StructField("interface", StringType())
                ])
                )
])

file_name = "/home/metrics"


#1. application metrics
#2. environment metrics
#1. environment metrics to detect application faults without app knoweldge
#2. two types of logs
#lttng logs and ordinary text file logs

df_disk = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics[0]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema_disk).alias("data")) \
    .select("data.timestamp", "data.tags.host", "data.name",
            round("data.fields.used_percent", 2).alias("used_percent")) \
    .withWatermark("timestamp", "30 seconds")
#    .select("data.*")
df_disk.printSchema()

formatted_df_disk = df_disk \
    .withColumn("year", year("timestamp")) \
    .withColumn("month", month("timestamp")) \
    .withColumn("day", dayofmonth("timestamp")) \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("append") \
    .format("csv") \
    .option("header", "true") \
    .option("path", file_name) \
    .option("checkpointLocation", "/home/checkpoint/dir") \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

df_mem = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics[1]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema_mem).alias("data")) \
    .select("data.timestamp", "data.tags.host", "data.name",
            round("data.fields.used_percent", 2).alias("used_percent")) \
    .withWatermark("timestamp", "30 seconds")
df_mem.printSchema()

formatted_df_mem = df_mem \
    .withColumn("year", year("timestamp")) \
    .withColumn("month", month("timestamp")) \
    .withColumn("day", dayofmonth("timestamp")) \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("append") \
    .format("csv") \
    .option("header", "true") \
    .option("path", file_name) \
    .option("checkpointLocation", "/home/checkpoint/dir") \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()


df_net = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics[3]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema_net).alias("data")) \
    .select("data.timestamp", "data.tags.host", "data.name",
            "data.fields.bytes_recv", "data.fields.bytes_sent", "data.fields.drop_in",
            "data.fields.drop_out", "data.fields.err_in", "data.fields.err_out",
            "data.fields.packets_recv", "data.fields.packets_sent") \
    .withWatermark("timestamp", "30 seconds")
#    .select("data.*")
df_net.printSchema()

formatted_df_net = df_net \
    .withColumn("year", year("timestamp")) \
    .withColumn("month", month("timestamp")) \
    .withColumn("day", dayofmonth("timestamp")) \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("append") \
    .format("csv") \
    .option("header", "true") \
    .option("path", file_name) \
    .option("checkpointLocation", "/home/checkpoint/dir") \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

formatted_df_disk.awaitTermination()
formatted_df_mem.awaitTermination()
formatted_df_net.awaitTermination()

#spark.streams.awaitAnyTermination()
