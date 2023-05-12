from pyspark.sql import SparkSession
from pyspark.sql.streaming import *

spark = SparkSession \
    .builder \
    .appName("Spark Kafka Streaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "bitnami-kafka-headless.observability.svc.cluster.local:9092") \
    .option("subscribe", "telegraf_disk") \
    .option("startingOffsets", "earliest") \
    .load()

df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

query = df \
    .writeStream \
    .outputMode("update") \
    .format("console") \
    .start()

# raw = spark.sql("select * from `kafka-streaming-messages`")
# raw.show()

query.awaitTermination()