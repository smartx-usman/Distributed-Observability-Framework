from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, LongType, DoubleType

spark = SparkSession.builder.appName("KafkaStreamReader").getOrCreate()

# Define schema for topic1
#schema_topic1 = StructType() \
#    .add("name", StringType()) \
#    .add("age", IntegerType())

# Define schema for topic2
#schema_topic2 = StructType() \
#    .add("id", IntegerType()) \
#    .add("address", StringType()) \
#    .add("city", StringType())

# Define Kafka connection details
kafka_bootstrap_servers = "bitnami-kafka-headless.observability.svc.cluster.local:9092"
topic1 = "telegraf_disk"
topic2 = "telegraf_mem"

schema_topic1 = StructType([
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

schema_topic2 = StructType([
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

# Read from topic1 with schema_topic1
df_topic1 = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", topic1) \
    .option("startingOffsets", "earliest") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema_topic1).alias("data")) \
    .select("data.*")

# Read from topic2 with schema_topic2
df_topic2 = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", topic2) \
    .option("startingOffsets", "earliest") \
    .load() \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema_topic2).alias("data")) \
    .select("data.*")

# Process the data from both topics as per your requirement
# You can perform join, aggregation or any other transformation

# Start the streaming query to write the data to Elasticsearch
query = df_topic1 \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 50) \
    .start()

query2 = df_topic2 \
    .writeStream \
    .trigger(processingTime='30 seconds') \
    .outputMode("Append") \
    .format("console") \
    .option("truncate", "false") \
    .option("numRows", 50) \
    .start()

spark.streams.awaitAnyTermination()