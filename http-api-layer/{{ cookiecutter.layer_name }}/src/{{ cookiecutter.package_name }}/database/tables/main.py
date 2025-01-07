from app import settings
from app.integrations.dynamodb import dynamodb_resource

main_table = dynamodb_resource.Table(settings.MAIN_TABLE_NAME)
