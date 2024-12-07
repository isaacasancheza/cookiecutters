from os import environ

import sentry_sdk
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

SENTRY_DSN = environ['SENTRY_DSN']
SENTRY_ENVIRONMENT = environ['SENTRY_ENVIRONMENT']

sentry_sdk.init(
    dsn=SENTRY_DSN,
    environment=SENTRY_ENVIRONMENT,
    integrations=[
        AwsLambdaIntegration(
            timeout_warning=True,
        ),
    ],
)

logger = Logger()


@logger.inject_lambda_context(clear_state=True)
def handler(event: dict, context: LambdaContext):
    pass
