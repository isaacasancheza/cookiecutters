from boto3 import client, resource

from app import settings

dynamodb = client('dynamodb', config=settings.BOTO3_CONFIG)
dynamodb_resource = resource('dynamodb', config=settings.BOTO3_CONFIG)
