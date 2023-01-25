import json
import logging
import time
import pandas as pd
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from aws import SQS, S3
from main import TOPICS

THRESHOLD = 5
BUCKET_NAME = "api-requests-to-data-lake"
FILEPATH = "test"


def create_aws_resources():
    # Check if the bucket already exists
    try:
        S3.head_bucket(Bucket=BUCKET_NAME)
    except S3.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error
        # If it was a 404 error, then the bucket does not exist
        error_code = int(e.response["Error"]["Code"])
        if error_code == 404:
            # Create the bucket
            S3.create_bucket(Bucket=BUCKET_NAME)
            logging.info(f"Bucket {BUCKET_NAME} created.")
        else:
            # If the error code is not 404, then raise the error
            raise e
    else:
        logging.info(f"Bucket {BUCKET_NAME} already exists.")

    # Create the queue
    for topic in TOPICS:
        response = SQS.create_queue(QueueName=topic)

        # Print the queue URL
        queue_url = response["QueueUrl"]
        logging.info(f"Queue {topic} created successfully with URL: {queue_url}")


def run_queue(topic):
    response = SQS.get_queue_url(QueueName=topic)
    queue_url = response["QueueUrl"]

    while True:
        response = SQS.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=["ApproximateNumberOfMessages"]
        )

        # Extract the approximate number of messages from the response
        approximate_number_of_messages = int(
            response["Attributes"]["ApproximateNumberOfMessages"]
        )

        # Print the approximate number of messages
        logging.info(
            f"Number of messages in the queue {queue_url}: {approximate_number_of_messages}"
        )

        # Extract the data from the messages

        if approximate_number_of_messages >= THRESHOLD:
            response = SQS.receive_message(
                QueueUrl=queue_url, MaxNumberOfMessages=approximate_number_of_messages
            )
            messages = response.get("Messages", [])

            # Extract the message body
            message_bodies = [json.loads(message["Body"]) for message in messages]

            # Convert the data to a Pandas DataFrame
            df = pd.DataFrame(message_bodies)

            # Convert the DataFrame to the Parquet format
            parquet_buffer = BytesIO()
            df.to_parquet(parquet_buffer)
            parquet_buffer.seek(0)

            # Push the Parquet data to the S3 bucket
            ts = time.time()
            S3.put_object(
                Bucket=BUCKET_NAME,
                Key=f"{topic}/{ts}.parquet",
                Body=parquet_buffer.read(),
            )

            # delete the messages
            for message in messages:
                SQS.delete_message(
                    QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"]
                )

            logging.info(
                "Data pulled from SQS, aggregated, converted to Parquet and pushed to S3 successfully!"
            )
        time.sleep(10)


create_aws_resources()

with ThreadPoolExecutor() as executor:
    # Submit the function for each queue URL
    results = [executor.submit(run_queue, topic) for topic in TOPICS]
    for f in results:
        f.result()
