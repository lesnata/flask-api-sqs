import json
import datetime
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask, request, jsonify
from aws import SQS

app = Flask(__name__)
limiter = Limiter(key_func=get_remote_address)
TOPICS = ['CleanMyMac', 'ClearVPN', 'CleanMyPC', 'CleanMyDrive']


@app.route("/track", methods=["POST"])
@limiter.limit("1000 per second")
def track():

    data = request.get_json()

    if not all(key in data for key in ("user_id", "app_name", "event_category")):
        return jsonify({"error": "Invalid JSON data"}), 400

    if data.get("app_name") not in TOPICS:
        return (
            jsonify(
                {
                    "error": f"Invalid app_name JSON data, possible values: {TOPICS}"
                }
            ),
            400,
        )

    data = {
        "user_id": data.get("user_id"),
        "app_name": data.get("app_name"),
        "event_category": data.get("event_category"),
        "event_value": data.get("event_value"),
        "event_time": datetime.datetime.now().isoformat(),
    }

    queue_url = SQS.get_queue_url(QueueName=data.get("app_name"))["QueueUrl"]

    SQS.send_message(QueueUrl=queue_url, MessageBody=json.dumps(data))
    return jsonify({"message": "Data sent to SQS successfully!"})


if __name__ == "__main__":
    app.run(debug=True)
