import os

from boto3 import Session

session = Session(
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    region_name=os.environ["AWS_REGION"],
)

SQS = session.client("sqs")

# Create an S3 client
S3 = session.client("s3")
