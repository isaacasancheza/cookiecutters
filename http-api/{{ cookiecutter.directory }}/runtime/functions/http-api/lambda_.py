import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

sentry_sdk.init(
    integrations=[
        AwsLambdaIntegration(
            timeout_warning=True,
        ),
    ],
    default_integrations=False,
)

from http import HTTPStatus
from typing import Any

from app import settings
from app.api import exceptions
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import (
    APIGatewayHttpResolver,
    CORSConfig,
    Response,
    content_types,
)
from aws_lambda_powertools.event_handler.openapi.exceptions import (
    RequestValidationError,
)
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()

app = APIGatewayHttpResolver(
    cors=CORSConfig(
        allow_origin=settings.CORS_ALLOW_ORIGIN,
    ),
    enable_validation=True,
)


@logger.inject_lambda_context(
    clear_state=True,
    correlation_id_path=correlation_paths.API_GATEWAY_HTTP,
)
def handler(event: dict, context: LambdaContext) -> dict[str, Any]:
    logger.append_keys(
        route_key=event['routeKey'],
        path_parameters=event.get('pathParameters', {}),
        query_string_parameters=event.get('queryStringParameters', {}),
    )
    return app.resolve(event, context)


@app.exception_handler(Exception)
def exception_handler(exception: Exception):
    if isinstance(exception, exceptions.ServiceError):
        return Response(
            body={
                'message': exception.msg,
                'statusCode': exception.status_code,
            },
            status_code=exception.status_code,
            content_type=content_types.APPLICATION_JSON,
        )
    elif isinstance(exception, RequestValidationError):
        errors = [{'loc': e['loc'], 'type': e['type']} for e in exception.errors()]
        return Response(
            body={
                'detail': errors,
                'statusCode': HTTPStatus.UNPROCESSABLE_ENTITY,
            },
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content_type=content_types.APPLICATION_JSON,
        )

    # log to cloudwatch
    logger.exception(exception)

    # send to sentry
    sentry_sdk.capture_exception(exception)

    raise exceptions.ServiceError(500, 'Internal Server Error')
