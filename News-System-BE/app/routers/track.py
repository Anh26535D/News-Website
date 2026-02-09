import os
from flask import Blueprint, request, jsonify
from app.service.kafka import KafkaPushService

# Load cấu hình từ môi trường
BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_API_KEY = os.environ.get("KAFKA_API_KEY")
KAFKA_API_SECRET = os.environ.get("KAFKA_API_SECRET")
TRACKING_TOPIC = os.environ.get("KAFKA_TRACKING_TOPIC", "user_activities")

track_blueprint = Blueprint("track", __name__)

# Khởi tạo Kafka Service (Sử dụng class chuyên nghiệp đã viết trước đó)
kafka_service = KafkaPushService(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    api_key=KAFKA_API_KEY,
    api_secret=KAFKA_API_SECRET,
)


@track_blueprint.route("", methods=["POST"])
def track_user_activity():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing tracking data"}), 400
        user_id = data.get("user_id", None)
        kafka_service.push(topic=TRACKING_TOPIC, obj=data, key=user_id)

        return jsonify({"status": "success", "message": "Event tracked"}), 202

    except Exception as e:
        print(f"Error tracking event: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
