from boto3 import client, resource

dynamodb = client('dynamodb')
dynamodb_resource = resource('dynamodb')
