import os

import boto3

bucketName = 'jszmidla-chatapp'

session = boto3.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET_KEY'],
)
s3 = session.resource('s3')


def save(pathFileName, metadata, body):
    s3.Object(bucketName, pathFileName).put(Body=body, Metadata=metadata)


def remove(pathFileName):
    s3.Object(bucketName, pathFileName).delete()
