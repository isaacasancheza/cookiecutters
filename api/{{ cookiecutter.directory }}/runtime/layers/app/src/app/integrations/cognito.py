from boto3 import client

from app import settings

cognito = client('cognito-idp', config=settings.BOTO3_CONFIG)
