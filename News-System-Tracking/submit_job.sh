spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3,org.mongodb.spark:mongo-spark-connector_2.13:10.1.1 spark_stream_consumer.py
