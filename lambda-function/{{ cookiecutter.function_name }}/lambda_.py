import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

sentry_sdk.init(
    integrations=[
        AwsLambdaIntegration(
            timeout_warning=True,
        ),
    ],
)

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger()


@logger.inject_lambda_context(
    clear_state=True,
)
def handler(event: dict, context: LambdaContext):
    pass
