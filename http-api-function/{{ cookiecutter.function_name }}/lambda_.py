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
from app.api import exceptions, routers
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import (
    APIGatewayHttpResolver,
    CORSConfig,
    Response,
    content_types,
)
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()
tracer = Tracer()

app = APIGatewayHttpResolver(
    cors=CORSConfig(
        allow_origin=settings.CORS_ALLOW_ORIGIN,
    ),
    enable_validation=True,
)

app.include_router(routers.auth.router, prefix='/auth')
app.include_router(routers.branches.router, prefix='/branches')
app.include_router(routers.businesses.router, prefix='/businesses')
app.include_router(routers.categories.router, prefix='/categories')
app.include_router(routers.domains.router, prefix='/domains')
app.include_router(routers.entities.router, prefix='/entities')
app.include_router(routers.items.router, prefix='/items')
app.include_router(routers.plans.router, prefix='/plans')
app.include_router(routers.status.router, prefix='/status')
app.include_router(routers.subcategories.router, prefix='/subcategories')
app.include_router(routers.suspensions.router, prefix='/suspensions')
app.include_router(routers.users.router, prefix='/users')


@logger.inject_lambda_context(
    clear_state=True,
    correlation_id_path=correlation_paths.API_GATEWAY_HTTP,
)
@tracer.capture_lambda_handler
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
    elif isinstance(exception, exceptions.RequestValidationError):
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
