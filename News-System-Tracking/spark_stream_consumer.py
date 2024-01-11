import sys
sys.path.append("/app")
import os

# import findspark
# findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import *
from dotenv import load_dotenv
load_dotenv()


KAFKA_TOPIC_NAME = "tracking"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9094"

mongo_uri = "mongodb://localhost:27017"
mongo_db = "tracking_db"
mongo_collection = "tracking_collection"

scala_version = '2.12'
spark_version = '3.3.3'
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    # 'org.apache.kafka:kafka-clients:3.4.0'
    'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1'
]

event_schema = StructType([
    StructField("isTrusted", BooleanType()),
    StructField("sessionTime", IntegerType())
])

main_schema = StructType([
    StructField("sessionId", StringType()),
    StructField("event", StringType(), True)
])

if __name__ == "__main__":
    spark = (
        SparkSession.builder.appName("TrackingDataConsumer").master('local[2]')
        # .master("spark://spark-master:7077")
        .config("spark.jars.packages", ",".join(packages)) \
        .config("spark.mongodb.input.uri", mongo_uri) \
        .config("spark.mongodb.output.uri", mongo_uri) \
        .getOrCreate()
    )
    
    print("Create sparck success")
    spark.sparkContext.setLogLevel("ERROR")

    trackingDataFrame = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", KAFKA_TOPIC_NAME) \
        .load()
  
    print("trackingDataFrame",trackingDataFrame)	
  
    # trackingDataFrame = trackingDataFrame.select(col("value").cast("string").alias("data"))

    inputStream = trackingDataFrame.selectExpr("CAST(value AS STRING) as json")
    structured_df = inputStream.select(from_json(col("json"), main_schema).alias("data")).select("data.*")
    structured_df = structured_df.withColumn("event", from_json(col("event"), event_schema))

    def write_to_mongo(df, epoch_id):
        df.write.format("mongo") \
            .mode("append") \
            .option("database", mongo_db) \
            .option("collection", mongo_collection) \
            .save()
        print(f"Batch {epoch_id} written to MongoDB")
    

    query = structured_df \
        .writeStream \
        .foreachBatch(write_to_mongo) \
        .outputMode("append") \
        .start()

    print("query",query)

    query.awaitTermination()
