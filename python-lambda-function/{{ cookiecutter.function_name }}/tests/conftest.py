from aws_lambda_powertools.utilities.typing import LambdaContext as _LambdaContext
from pytest import fixture


class LambdaContext(_LambdaContext):
    _function_name = 'test'
    _memory_limit_in_mb = 128
    _invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789012:function:test'
    _aws_request_id = 'da658bd3-2d6f-4e7b-8ec2-937234644fdc'


@fixture
def lambda_context() -> LambdaContext:
    return LambdaContext()
