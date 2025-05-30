from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode, split
from pyspark.sql.types import StructType, StringType

# Define schema for tweet JSON
schema = StructType() \
    .add("tweet_id", StringType()) \
    .add("user", StringType()) \
    .add("airline", StringType()) \
    .add("sentiment", StringType()) \
    .add("text", StringType()) \
    .add("timestamp", StringType())

# Initialize Spark session
spark = SparkSession.builder \
    .appName("TwitterKafkaSpark") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read data from Kafka
df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "tweets_topic") \
    .load()

# Convert Kafka value (bytes) to string and then parse JSON
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Extract and analyze words from tweets
words = json_df.select(explode(split(col("text"), " ")).alias("word"))
word_counts = words.groupBy("word").count()

query = word_counts.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .option("numRows", 50) \
    .start()

query.awaitTermination()

