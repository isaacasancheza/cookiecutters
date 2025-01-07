import aws_cdk as cdk
from aws_cdk import aws_lambda as lambda_
from constructs import Construct


class Layer(lambda_.LayerVersion):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        source_code_directory: str,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            code=lambda_.Code.from_asset(
                path=f'../../runtime/layers/{source_code_directory}',
                bundling=cdk.BundlingOptions(
                    image=lambda_.Runtime.PYTHON_{{ cookiecutter._runtime_python_version }}.bundling_image,
                    command=[
                        'bash',
                        '-c',
                        'pip install --no-cache-dir -r requirements.txt -t /asset-output/python && rsync -r src /asset-output/python',
                    ],
                ),
            ),
            compatible_runtimes=[
                lambda_.Runtime.PYTHON_{{ _runtime_python_version }},
            ],
            compatible_architectures=[
                lambda_.Architecture.ARM_64,
            ],
        )


class Layers(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
    ) -> None:
        super().__init__(scope, construct_id)
        app = Layer(
            self,
            'App',
            source_code_directory='app',
        )

        self.app = app
