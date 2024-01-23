from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler.router import APIGatewayHttpRouter


logger = Logger()
router = APIGatewayHttpRouter()
