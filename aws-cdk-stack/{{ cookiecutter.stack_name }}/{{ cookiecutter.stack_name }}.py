import aws_cdk as cdk
from constructs import Construct


class {{ cookiecutter.stack_name.split('_') | map('capitalize') | join('') }}Stack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
