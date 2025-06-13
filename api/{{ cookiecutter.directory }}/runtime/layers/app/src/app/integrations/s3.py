from boto3 import client

from app import settings

s3 = client('s3', config=settings.BOTO3_CONFIG)
