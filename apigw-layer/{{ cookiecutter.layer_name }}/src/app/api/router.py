from typing import Any

from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.utilities.typing import LambdaContext

from app.api import routers

app = APIGatewayHttpResolver(enable_validation=True)


@logger.inject_lambda_context(clear_state=True, correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def handler(event, context: LambdaContext) -> dict[str, Any]:
    return app.resolve(event, context)
