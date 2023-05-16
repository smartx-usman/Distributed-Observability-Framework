import logging
import os
from datetime import datetime

from pyspark.sql import SparkSession
from pyspark.sql.functions import round, col, from_json

import schemas
import topics as topics_list

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Get the Elasticsearch, Kafka broker, and topic
kafka_broker = os.environ['KAFKA_BROKER']
es_nodes = os.environ['ES_NODES']

window_size, window_slide, threshold = 30, 10, 2

# file_name = "/home/metrics"
data_dir = "/home"
checkpoint_dir = f'{data_dir}/checkpoint/dir'

logging.info(f'Number of Kafka topic to start reading data: {len(topics_list.topics)}.')

# Create directories for storing data
for directory in ["disk", "diskio", "mem", "cpu", "net", "system", "k8s_pod_con", "k8s_pod_net", "k8s_pod_vol",
                  "k8s_pod_deployment", "k8s_pod_daemonset", "k8s_pod_statefulset", "k8s_pod_service"]:
    if not os.path.exists(f"{data_dir}/{directory}"):
        os.makedirs(f"{data_dir}/{directory}")

# Create a SparkSessions
spark = SparkSession \
    .builder \
    .appName("MetricsStream") \
    .config("spark.sql.streaming.statefulOperator.checkCorrectness.enabled", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Disk metrics stream processing
input_disk = spark \
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
input_disk.printSchema()


def process_disk(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    # df.write.mode("append").csv(data_dir + "/disk-" + timestamp)
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/disk/" + timestamp + ".csv", mode='a', index=False)


formatted_df_disk = input_disk \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_disk) \
    .outputMode("append") \
    .start()

# query_disk = input_disk \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("Append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .option("numRows", 10) \
#     .start()

# Diskio metrics stream processing
input_diskio = spark \
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

input_diskio.printSchema()


def process_diskio(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    # df.write.mode("append").csv(data_dir + "/diskio-" + timestamp)
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/diskio/" + timestamp + ".csv", mode='a', index=False)


formatted_df_diskio = input_diskio \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_diskio) \
    .outputMode("append") \
    .start()

# query_diskio = df_diskio \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("Append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .option("numRows", 10) \
#     .start()

# Memory metrics stream processing
input_mem = spark \
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
input_mem.printSchema()


# formatted_df_mem = input_mem \
#     .withColumn("year", year("timestamp")) \
#     .withColumn("month", month("timestamp")) \
#     .withColumn("day", dayofmonth("timestamp")) \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("append") \
#     .format("csv") \
#     .option("header", "true") \
#     .option("path", data_dir + "/mem") \
#     .option("checkpointLocation", checkpoint_dir) \
#     .option("truncate", "false") \
#     .start()


def process_mem(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    # df.write.mode("append").csv(data_dir + "/diskio-" + timestamp)
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/mem/" + timestamp + ".csv", mode='a', index=False)


formatted_df_mem = input_mem \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_mem) \
    .outputMode("append") \
    .start()

# query_mem = df_mem \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("Append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .option("numRows", 10) \
#     .start()

# CPU metrics stream processing
input_cpu = spark \
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

input_cpu.printSchema()


# formatted_df_cpu = input_cpu \
#     .withColumn("year", year("timestamp")) \
#     .withColumn("month", month("timestamp")) \
#     .withColumn("day", dayofmonth("timestamp")) \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("append") \
#     .format("csv") \
#     .option("header", "true") \
#     .option("path", data_dir) \
#     .option("checkpointLocation", checkpoint_dir) \
#     .partitionBy("name", "year", "month", "day") \
#     .option("truncate", "false") \
#     .start()


def process_cpu(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    # df.write.mode("append").csv(data_dir + "/diskio-" + timestamp)
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/cpu/" + timestamp + ".csv", mode='a', index=False)


formatted_df_cpu = input_cpu \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_cpu) \
    .outputMode("append") \
    .start()

# query_cpu = df_cpu \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("Append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .option("numRows", 10) \
#     .start()

# Network metrics stream processing
input_net = spark \
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

input_net.printSchema()


# formatted_df_net = input_net \
#     .withColumn("year", year("timestamp")) \
#     .withColumn("month", month("timestamp")) \
#     .withColumn("day", dayofmonth("timestamp")) \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("append") \
#     .format("csv") \
#     .option("header", "true") \
#     .option("path", data_dir) \
#     .option("checkpointLocation", checkpoint_dir) \
#     .partitionBy("name", "year", "month", "day") \
#     .option("truncate", "false") \
#     .start()


def process_net(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    # df.write.mode("append").csv(data_dir + "/diskio-" + timestamp)
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/net/" + timestamp + ".csv", mode='a', index=False)


formatted_df_net = input_net \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_net) \
    .outputMode("append") \
    .start()

# query_net = df_net \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("Append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .option("numRows", 10) \
#     .start()

# System load metrics stream processing
input_system = spark \
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

input_system.printSchema()


# formatted_df_system = input_system \
#     .withColumn("year", year("timestamp")) \
#     .withColumn("month", month("timestamp")) \
#     .withColumn("day", dayofmonth("timestamp")) \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("append") \
#     .format("csv") \
#     .option("header", "true") \
#     .option("path", data_dir) \
#     .option("checkpointLocation", checkpoint_dir) \
#     .partitionBy("name", "year", "month", "day") \
#     .option("truncate", "false") \
#     .start()


def process_system(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    # df.write.mode("append").csv(data_dir + "/diskio-" + timestamp)
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/system/" + timestamp + ".csv", mode='a', index=False)


formatted_df_system = input_system \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_system) \
    .outputMode("append") \
    .start()

# query_system = df_system \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("Append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .option("numRows", 10) \
#     .start()

# K8S pod container usage metrics stream processing
input_k8s_pod_con = spark \
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

input_k8s_pod_con.printSchema()


def process_k8s_pod_con(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    # df.write.mode("append").csv(data_dir + "/diskio-" + timestamp)
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/k8s_pod_con/" + timestamp + ".csv", mode='a', index=False)


formatted_df_k8s_pod_con = input_k8s_pod_con \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_k8s_pod_con) \
    .outputMode("append") \
    .start()

# formatted_df_k8s_pod_con = input_k8s_pod_con \
#     .withColumn("year", year("timestamp")) \
#     .withColumn("month", month("timestamp")) \
#     .withColumn("day", dayofmonth("timestamp")) \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("append") \
#     .format("csv") \
#     .option("header", "true") \
#     .option("path", data_dir) \
#     .option("checkpointLocation", checkpoint_dir) \
#     .partitionBy("name", "year", "month", "day") \
#     .option("truncate", "false") \
#     .start()

# query_k8s_pod_con = df_k8s_pod_con \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("Append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .option("numRows", 10) \
#     .start()

# K8S pod network usage metrics stream processing
input_k8s_pod_net = spark \
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

input_k8s_pod_net.printSchema()


# formatted_df_k8s_pod_net = input_k8s_pod_net \
#     .withColumn("year", year("timestamp")) \
#     .withColumn("month", month("timestamp")) \
#     .withColumn("day", dayofmonth("timestamp")) \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("append") \
#     .format("csv") \
#     .option("header", "true") \
#     .option("path", data_dir) \
#     .option("checkpointLocation", checkpoint_dir) \
#     .partitionBy("name", "year", "month", "day") \
#     .option("truncate", "false") \
#     .start()


def process_k8s_pod_net(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    # df.write.mode("append").csv(data_dir + "/diskio-" + timestamp)
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/k8s_pod_net/" + timestamp + ".csv", mode='a', index=False)


formatted_df_k8s_pod_net = input_k8s_pod_net \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_k8s_pod_net) \
    .outputMode("append") \
    .start()

# query_k8s_pod_net = df_k8s_pod_net \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("Append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .option("numRows", 10) \
#     .start()


# K8S pod volume usage metrics stream processing
input_k8s_pod_vol = spark \
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

input_k8s_pod_vol.printSchema()


# formatted_df_k8s_pod_vol = input_k8s_pod_vol \
#     .withColumn("year", year("timestamp")) \
#     .withColumn("month", month("timestamp")) \
#     .withColumn("day", dayofmonth("timestamp")) \
#     .writeStream \
#     .trigger(processingTime='30 seconds') \
#     .outputMode("append") \
#     .format("csv") \
#     .option("header", "true") \
#     .option("path", data_dir) \
#     .option("checkpointLocation", checkpoint_dir) \
#     .partitionBy("name", "year", "month", "day") \
#     .option("truncate", "false") \
#     .start()


def process_k8s_pod_vol(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    # df.write.mode("append").csv(data_dir + "/diskio-" + timestamp)
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/k8s_pod_vol/" + timestamp + ".csv", mode='a', index=False)


formatted_df_k8s_pod_vol = input_k8s_pod_vol \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_k8s_pod_vol) \
    .outputMode("append") \
    .start()

query_k8s_pod_vol = input_k8s_pod_vol \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 10) \
    .start()

# K8S daemonset metrics stream processing
input_k8s_daemonset = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[11]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_k8s_daemonset).alias("data")) \
    .select("data.timestamp", "data.name",
            "data.tags.namespace", "data.tags.daemonset_name",
            "data.fields.created", "data.fields.generation",
            "data.fields.number_available", "data.fields.number_unavailable",
            "data.fields.desired_number_scheduled", "data.fields.number_misscheduled", "data.fields.number_ready",
            "data.fields.updated_number_scheduled", "data.fields.current_number_scheduled") \
    .withWatermark("timestamp", "30 seconds")

input_k8s_daemonset.printSchema()


def process_k8s_daemonset(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/k8s_pod_daemonset/" + timestamp + ".csv", mode='a', index=False)


formatted_df_k8s_daemonset = input_k8s_daemonset \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_k8s_daemonset) \
    .outputMode("append") \
    .start()

# K8S deployment metrics stream processing
input_k8s_deployment = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[12]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_k8s_deployment).alias("data")) \
    .select("data.timestamp", "data.name",
            "data.tags.namespace", "data.tags.deployment_name", "data.tags.host",
            "data.fields.created", "data.fields.replicas_available", "data.fields.replicas_unavailable") \
    .withWatermark("timestamp", "30 seconds")

input_k8s_deployment.printSchema()


def process_k8s_deployment(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/k8s_pod_deployment/" + timestamp + ".csv", mode='a', index=False)


formatted_df_k8s_deployment = input_k8s_deployment \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_k8s_deployment) \
    .outputMode("append") \
    .start()

# K8S statefulset metrics stream processing
input_k8s_statefulset = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[13]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_k8s_statefulset).alias("data")) \
    .select("data.timestamp", "data.name",
            "data.tags.namespace", "data.tags.statefulset_name",
            "data.fields.created", "data.fields.replicas", "data.fields.replicas_current", "data.fields.replicas_ready",
            "data.fields.replicas_updated", "data.fields.spec_replicas") \
    .withWatermark("timestamp", "30 seconds")

input_k8s_statefulset.printSchema()


def process_k8s_statefulset(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/k8s_pod_statefulset/" + timestamp + ".csv", mode='a', index=False)


formatted_df_statefulset = input_k8s_statefulset \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_k8s_statefulset) \
    .outputMode("append") \
    .start()

# K8S service metrics stream processing
input_k8s_service = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topics_list.topics[14]) \
    .option("startingOffsets", "latest") \
    .option("failOnDataLoss", "false") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schemas.schema_k8s_service).alias("data")) \
    .select("data.timestamp", "data.name",
            "data.tags.namespace", "data.tags.service_name",
            "data.fields.created", "data.fields.generation", "data.fields.port", "data.fields.target_port") \
    .withWatermark("timestamp", "30 seconds")

input_k8s_service.printSchema()


def process_k8s_service(df, batch_id):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H")
    pandas_df = df.toPandas()
    pandas_df.to_csv(data_dir + "/k8s_pod_service/" + timestamp + ".csv", mode='a', index=False)


formatted_df_k8s_pod_vol = input_k8s_service \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .foreachBatch(process_k8s_service) \
    .outputMode("append") \
    .start()

# formatted_df_disk.awaitTermination()
# formatted_df_mem.awaitTermination()
# formatted_df_net.awaitTermination()

spark.streams.awaitAnyTermination()
