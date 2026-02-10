import json
from confluent_kafka import Producer


class KafkaPushService:
    def __init__(self, bootstrap_servers, api_key, api_secret):
        self.config = {
            "bootstrap.servers": bootstrap_servers,
            "acks": "all",
            "retries": 5,
        }

        if api_key and api_secret:
            self.config.update(
                {
                    "security.protocol": "SASL_SSL",
                    "sasl.mechanisms": "PLAIN",
                    "sasl.username": api_key,
                    "sasl.password": api_secret,
                }
            )
        else:
            self.config.update({"security.protocol": "PLAINTEXT"})

        self.producer = Producer(self.config)
        self.producer = Producer(self.config)

    def _delivery_callback(self, err, msg):
        """Callback kiểm tra kết quả gửi tin nhắn."""
        if err:
            print(f"ERROR: Message failed delivery: {err}")
        else:
            key = msg.key().decode("utf-8") if msg.key() else "N/A"
            print(f"Produced to {msg.topic()}: key = {key:12} status = Delivered")

    def push(self, topic, obj, key=None):
        """
        Đẩy dữ liệu vào Kafka.
        :param topic: Tên topic
        :param obj: Dữ liệu (Dict/List) - sẽ được convert sang JSON
        :param key: Message key (Dùng để định danh hoặc phân vùng dữ liệu)
        """
        try:
            value = json.dumps(obj).encode("utf-8")
            message_key = str(key).encode("utf-8") if key else None
            self.producer.produce(
                topic=topic,
                value=value,
                key=message_key,
                callback=self._delivery_callback,
            )
            self.producer.poll(0)

        except Exception as e:
            print(f"Local error during produce: {e}")

    def flush(self):
        """Chờ gửi hết toàn bộ tin nhắn còn tồn đọng trong buffer."""
        print("Flushing outstanding messages...")
        self.producer.flush()
