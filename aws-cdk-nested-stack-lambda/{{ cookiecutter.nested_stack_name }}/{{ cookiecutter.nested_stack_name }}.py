import aws_cdk as cdk
from aws_cdk import aws_lambda as lambda_
from constructs import Construct


class LambdaLayer(Construct):
    def __init__(
            self, 
            scope: Construct, 
            construct_id: str, 
            /, 
            *, 
            is_package: bool = False, 
            source_code_path: str, 
            **kwargs,
        ) -> None:
        super().__init__(scope, construct_id)

        if is_package:
            command = ['bash', '-c', 'pip install . -t /asset-output/python']
        else:
            command = ['bash', '-c', 'pip install -r requirements.txt -t /asset-output/python']

        self.layer = lambda_.LayerVersion(
            self,
            construct_id,
            code=lambda_.Code.from_asset(source_code_path, bundling=cdk.BundlingOptions(
                image=lambda_.Runtime.PYTHON_3_11.bundling_image, 
                command=command,
            )),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            compatible_runtimes=[
                lambda_.Runtime.PYTHON_3_11,
            ],
            compatible_architectures=[
                lambda_.Architecture.X86_64,
            ],
            **kwargs,
        )


class LambdaFunction(Construct):
    def __init__(
            self, 
            scope: Construct, 
            construct_id: str,
            /, 
            *, 
            source_code_path: str, 
            timeout: int = 60, 
            **kwargs,
        ) -> None:
        super().__init__(scope, construct_id)

        self.function = lambda_.Function(
            self, 
            construct_id, 
            code=lambda_.Code.from_asset(source_code_path, bundling=cdk.BundlingOptions(
                image=lambda_.Runtime.PYTHON_3_11.bundling_image, 
                command=['bash', '-c', 'rsync -r . /asset-output'],
            )),
            handler='lambda.handler',
            timeout=cdk.Duration.seconds(timeout),
            tracing=lambda_.Tracing.ACTIVE,
            runtime=lambda_.Runtime.PYTHON_3_11,
            memory_size=512,
            **kwargs,
        )


class {{ cookiecutter.nested_stack_name.split('_') | map('capitalize') | join('') }}NestedStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
