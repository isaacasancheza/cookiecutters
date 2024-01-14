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
            source_code_path: str, 
            **kwargs,
        ) -> None:
        super().__init__(scope, construct_id)

        self.layer = lambda_.LayerVersion(
            self,
            construct_id,
            code=lambda_.Code.from_asset(source_code_path, bundling=cdk.BundlingOptions(
                image=lambda_.Runtime.PYTHON_3_12.bundling_image, 
                command=['bash', '-c', 'pip install -r requirements.txt -t /asset-output/python'],
            )),
            compatible_runtimes=[
                lambda_.Runtime.PYTHON_3_11,
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
            handler: str = 'lambda_.handler',
            source_code_path: str, 
            **kwargs,
        ) -> None:
        super().__init__(scope, construct_id)

        self.function = lambda_.Function(
            self, 
            construct_id, 
            code=lambda_.Code.from_asset(source_code_path, bundling=cdk.BundlingOptions(
                image=lambda_.Runtime.PYTHON_3_12.bundling_image, 
                command=['bash', '-c', 'rsync -r . /asset-output'],
            )),
            handler='lambda.handler',
            runtime=lambda_.Runtime.PYTHON_3_12,
            **kwargs,
        )


class {{ cookiecutter.nested_stack_name.split('_') | map('capitalize') | join('') }}NestedStack(cdk.NestedStack):
    def __init__(
            self, 
            scope: Construct, 
            construct_id: str,
            /,
            **kwargs,
        ) -> None:
        super().__init__(scope, construct_id, **kwargs)
