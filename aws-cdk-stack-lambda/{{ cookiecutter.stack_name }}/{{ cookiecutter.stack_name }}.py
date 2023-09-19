import aws_cdk as cdk
from aws_cdk import aws_lambda as lambda_
from constructs import Construct


class LambdaFunction(Construct):
    def __init__(self, scope: Construct, construct_id: str, source_code_path: str, timeout: int = 60) -> None:
        super().__init__(scope, construct_id)

        self.function: lambda_.Function = lambda_.Function(
            self, 
            construct_id, 
            code=lambda_.Code.from_asset(source_code_path, bundling=cdk.BundlingOptions(
                image=lambda_.Runtime.PYTHON_3_10.bundling_image, 
                command=['bash', '-c', 'pip install -r requirements.txt -t /asset-output && cp -au . /asset-output',
            ])),
            handler='lambda.handler',
            timeout=cdk.Duration.seconds(timeout),
            tracing=lambda_.Tracing.ACTIVE,
            runtime=lambda_.Runtime.PYTHON_3_11,
        )


class {{ cookiecutter.stack_name.split('_') | map('capitalize') | join('') }}Stack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
