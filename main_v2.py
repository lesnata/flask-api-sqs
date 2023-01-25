# import time
# import datetime
# from io import BytesIO
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# from flask import Flask, request, jsonify
# from queue_manager import BUCKET_NAME
# from queue_manager import TOPICS
# from request_holder import RequestHolder
# from aws import S3
#
#
# app2 = Flask(__name__)
# limiter = Limiter(key_func=get_remote_address)
#
# THRESHOLD = 5
# holder = RequestHolder()
#
#
# @app2.route("/track", methods=["POST"])
# @limiter.limit("1000 per second")
# def track():
#
#     data = request.get_json()
#
#     if not all(key in data for key in ("user_id", "app_name", "event_category")):
#         return jsonify({"error": "Invalid JSON data"}), 400
#
#     if data.get("app_name") not in TOPICS:
#         return (
#             jsonify(
#                 {
#                     "error": f"Invalid app_name JSON data, possible values: {TOPICS}"
#                 }
#             ),
#             400,
#         )
#
#     data = {
#         "user_id": data.get("user_id"),
#         "app_name": data.get("app_name"),
#         "event_category": data.get("event_category"),
#         "event_value": data.get("event_value"),
#         "event_time": datetime.datetime.now().isoformat(),
#     }
#
#     # Append the new data to the existing DataFrame
#     holder.append(data=data)
#
#     # Check if we've received 100 requests
#     if len(holder.requests_pull) >= THRESHOLD:
#
#         buffer = BytesIO()
#         holder.requests_pull.to_parquet(buffer, index=False)
#
#         ts = time.time()
#
#         # s3.upload_file('data.parquet', 'my-bucket', 'data.parquet')
#         S3.put_object(Bucket=BUCKET_NAME, Key=f"aggregated/{ts}.parquet", Body=buffer.getvalue())
#         print(f"RequestHolder is pushed to s3 parquet file")
#         # Clear the DataFrame for the next batch of data
#         holder.truncate()
#         print(f"RequestHolder is truncated")
#
#     return "Request submitted successfully"
#
#
# if __name__ == "__main__":
#     app2.run(debug=True)
