import logging
import os

from pyspark.sql import SparkSession
from pyspark.sql.functions import round, col, from_json, year, month, dayofmonth

import schemas
import topics as topics_list

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get the Elasticsearch, Kafka broker, and topic
kafka_broker = os.environ['KAFKA_BROKER']
es_nodes = os.environ['ES_NODES']

window_size, window_slide, threshold = 30, 10, 2

logging.info(f'Number of Kafka topic to start reading data: {len(topics_list.topics)}.')

# Create a SparkSessions
spark = SparkSession \
    .builder \
    .appName("MetricsStream") \
    .config("spark.sql.streaming.statefulOperator.checkCorrectness.enabled", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# file_name = "/home/metrics"
data_dir = "/home"
checkpoint_dir = f'{data_dir}/checkpoint/dir'

# 1. application metrics
# 2. environment metrics
# 1. environment metrics to detect application faults without app knoweldge
# 2. two types of logs
# lttng logs and ordinary text file logs

# Disk metrics stream processing
df_disk = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[0]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_disk).alias("data")) \
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
    .option("path", data_dir) \
    .option("checkpointLocation", checkpoint_dir) \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

query_disk = df_disk \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .start()

# Diskio metrics stream processing
df_diskio = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[1]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_diskio).alias("data")) \
    .select("data.timestamp", "data.tags.host", "data.name", col("data.tags.name").alias("device_name"),
            "data.fields.io_time", "data.fields.read_time", "data.fields.reads",
            "data.fields.write_time", "data.fields.writes") \
    .withWatermark("timestamp", "30 seconds")

df_diskio.printSchema()

formatted_df_diskio = df_diskio \
    .withColumn("year", year("timestamp")) \
    .withColumn("month", month("timestamp")) \
    .withColumn("day", dayofmonth("timestamp")) \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("append") \
    .format("csv") \
    .option("header", "true") \
    .option("path", data_dir) \
    .option("checkpointLocation", checkpoint_dir) \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

query_diskio = df_diskio \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .start()

# Memory metrics stream processing
df_mem = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[2]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_mem).alias("data")) \
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
    .option("path", data_dir) \
    .option("checkpointLocation", checkpoint_dir) \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

query_mem = df_mem \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .start()

# CPU metrics stream processing
df_cpu = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[3]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_cpu).alias("data")) \
    .select("data.timestamp", "data.tags.host", "data.name", "data.tags.cpu",
            round("data.fields.usage_system", 2).alias("usage_system"),
            round("data.fields.usage_user", 2).alias("usage_user"),
            round("data.fields.usage_steal", 2).alias("usage_steal"),
            round("data.fields.usage_softirq", 2).alias("usage_softirq"),
            round("data.fields.usage_nice", 2).alias("usage_nice"),
            round("data.fields.usage_irq", 2).alias("usage_irq"),
            round("data.fields.usage_iowait", 2).alias("usage_iowait"),
            round("data.fields.usage_idle", 2).alias("usage_idle"),
            round("data.fields.usage_guest", 2).alias("usage_guest"),
            round("data.fields.usage_guest_nice", 2).alias("usage_guest_nice")) \
    .withWatermark("timestamp", "30 seconds")
df_cpu.printSchema()

formatted_df_cpu = df_cpu \
    .withColumn("year", year("timestamp")) \
    .withColumn("month", month("timestamp")) \
    .withColumn("day", dayofmonth("timestamp")) \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("append") \
    .format("csv") \
    .option("header", "true") \
    .option("path", data_dir) \
    .option("checkpointLocation", checkpoint_dir) \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

query_cpu = df_cpu \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .start()

# Network metrics stream processing
df_net = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[4]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_net).alias("data")) \
    .select("data.timestamp", "data.tags.host", "data.name",
            "data.fields.bytes_recv", "data.fields.bytes_sent", "data.fields.drop_in",
            "data.fields.drop_out", "data.fields.err_in", "data.fields.err_out",
            "data.fields.packets_recv", "data.fields.packets_sent") \
    .withWatermark("timestamp", "30 seconds")
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
    .option("path", data_dir) \
    .option("checkpointLocation", checkpoint_dir) \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

query_net = df_net \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .start()

# System load metrics stream processing
df_system = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[5]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_system).alias("data")) \
    .select("data.timestamp", "data.tags.host", "data.name",
            "data.fields.load1", "data.fields.load5", "data.fields.load15") \
    .withWatermark("timestamp", "30 seconds")
df_net.printSchema()

formatted_df_system = df_system \
    .withColumn("year", year("timestamp")) \
    .withColumn("month", month("timestamp")) \
    .withColumn("day", dayofmonth("timestamp")) \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("append") \
    .format("csv") \
    .option("header", "true") \
    .option("path", data_dir) \
    .option("checkpointLocation", checkpoint_dir) \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

query_system = df_system \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .start()

# K8S pod container usage metrics stream processing
df_k8s_pod_con = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[8]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_k8s_pod_cont).alias("data")) \
    .select("data.timestamp", "data.tags.host", "data.name", "data.tags.pod_name", "data.tags.namespace",
            "data.tags.container_name",
            "data.fields.cpu_usage_nanocores", "data.fields.cpu_usage_core_nanoseconds",
            "data.fields.memory_usage_bytes",
            "data.fields.memory_working_set_bytes", "data.fields.memory_rss_bytes", "data.fields.memory_page_faults",
            "data.fields.memory_major_page_faults", "data.fields.rootfs_available_bytes",
            "data.fields.rootfs_capacity_bytes",
            "data.fields.rootfs_used_bytes", "data.fields.logsfs_available_bytes", "data.fields.logsfs_capacity_bytes",
            "data.fields.logsfs_used_bytes", ) \
    .withWatermark("timestamp", "30 seconds")

df_k8s_pod_con.printSchema()

formatted_df_k8s_pod_con = df_k8s_pod_con \
    .withColumn("year", year("timestamp")) \
    .withColumn("month", month("timestamp")) \
    .withColumn("day", dayofmonth("timestamp")) \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("append") \
    .format("csv") \
    .option("header", "true") \
    .option("path", data_dir) \
    .option("checkpointLocation", checkpoint_dir) \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

query_k8s_pod_con = df_k8s_pod_con \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .start()

# K8S pod network usage metrics stream processing
df_k8s_pod_net = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[9]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_k8s_pod_net).alias("data")) \
    .select("data.timestamp", "data.tags.host", "data.name", "data.tags.pod_name", "data.tags.namespace",
            "data.fields.rx_bytes", "data.fields.rx_errors", "data.fields.tx_bytes", "data.fields.tx_errors") \
    .withWatermark("timestamp", "30 seconds")

df_k8s_pod_net.printSchema()

formatted_df_k8s_pod_net = df_k8s_pod_net \
    .withColumn("year", year("timestamp")) \
    .withColumn("month", month("timestamp")) \
    .withColumn("day", dayofmonth("timestamp")) \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("append") \
    .format("csv") \
    .option("header", "true") \
    .option("path", data_dir) \
    .option("checkpointLocation", checkpoint_dir) \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

query_k8s_pod_net = df_k8s_pod_net \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .start()

# K8S pod volume usage metrics stream processing
df_k8s_pod_vol = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[10]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_k8s_pod_vol).alias("data")) \
    .select("data.timestamp", "data.tags.host", "data.name", "data.tags.pod_name", "data.tags.namespace",
            "data.tags.volume_name",
            "data.fields.available_bytes", "data.fields.capacity_bytes", "data.fields.used_bytes") \
    .withWatermark("timestamp", "30 seconds")
df_k8s_pod_vol.printSchema()

formatted_df_k8s_pod_vol = df_k8s_pod_vol \
    .withColumn("year", year("timestamp")) \
    .withColumn("month", month("timestamp")) \
    .withColumn("day", dayofmonth("timestamp")) \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("append") \
    .format("csv") \
    .option("header", "true") \
    .option("path", data_dir) \
    .option("checkpointLocation", checkpoint_dir) \
    .partitionBy("name", "year", "month", "day") \
    .option("truncate", "false") \
    .start()

query_k8s_pod_vol = df_k8s_pod_vol \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .start()

# formatted_df_disk.awaitTermination()
# formatted_df_mem.awaitTermination()
# formatted_df_net.awaitTermination()

spark.streams.awaitAnyTermination()
