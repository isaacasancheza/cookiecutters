from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, Response
from aws_lambda_powertools.event_handler.middlewares import NextMiddleware

logger = Logger()


def authorizer(
    app: APIGatewayHttpResolver,
    next_middelware: NextMiddleware,
) -> Response:
    return next_middelware(app)
