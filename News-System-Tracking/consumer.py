import json
import os
from dotenv import load_dotenv
load_dotenv()

from confluent_kafka import Consumer
from pymongo import MongoClient

KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_CONSUMER_GROUP = os.environ.get("KAFKA_CONSUMER_GROUP")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC")

MONGO_URI = os.environ.get("MONGO_URI")
MONGO_DB = os.environ.get("MONGO_DB")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")

if __name__ == "__main__":
    mongo_client = MongoClient(MONGO_URI)
    mongo_db = mongo_client[MONGO_DB]
    mongo_collection = mongo_db[MONGO_COLLECTION]

    c = Consumer({
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": KAFKA_CONSUMER_GROUP,
        "auto.offset.reset": "earliest"
    })

    c.subscribe([KAFKA_TOPIC])

    try:
        while True:
            msg = c.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            
            json_data = json.loads(msg.value().decode("utf-8"))
            session_id = json_data["sessionId"]
            event = json_data["event"]

            if type(event) != dict:
                event = {"isConnectEvent": event}
                session_time = None
            else:
                event["isConnectEvent"] = "no"
                session_time = event["sessionTime"]

            key_to_extract = [
                "isConnectEvent",
                "isTrusted", 
                "screenX", "screenY", "clientX", "clientY", 
                "x", "y", 
                "timeStamp", 
                "target"
            ]
            processed_data = {key: event.get(key, None) for key in key_to_extract}
            processed_data["sessionId"] = session_id
            processed_data["sessionTime"] = session_time

            key_target_to_extract = [
                "tagName",
                "className",
                "id",
                "innerText",
            ]
            if processed_data["target"]:
                processed_data["target"] = {key: processed_data["target"].get(key, None) for key in key_target_to_extract}

            mongo_collection.insert_one(processed_data)
            print("Inserted data to MongoDB")
    except KeyboardInterrupt:
        pass
    finally:    
        c.close()
        mongo_client.close()