from typing import cast

import aws_cdk as cdk
import jsii
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from constructs import Construct

from stack_constructs.data import Data
from stack_constructs.layers import Layers


@jsii.implements(cdk.IAspect)
class ShareResources:
    def __init__(
        self,
        layers: Layers,
        project_name: str,
        sentry_dsn: str,
        sentry_environment: str,
    ) -> None:
        self._layers = layers
        self._project_name = project_name
        self._sentry_dsn = sentry_dsn
        self._sentry_environment = sentry_environment

    def visit(self, node: Construct) -> None:
        if isinstance(node, lambda_.Function):
            node.add_layers(
                self._layers.app,
            )

            node.add_environment('PROJECT_NAME', self._project_name)
            node.add_environment('SENTRY_DSN', self._sentry_dsn)
            node.add_environment('SENTRY_ENVIRONMENT', self._sentry_environment)

            # required by settings.py file
            node.add_to_role_policy(
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        'ssm:GetParametersByPath',
                    ],
                    resources=[
                        f'arn:{cdk.Aws.PARTITION}:ssm:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:parameter/{self._project_name}',
                    ],
                ),
            )


class Function(lambda_.Function):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        timeout: cdk.Duration = cdk.Duration.seconds(60),
        tracing: lambda_.Tracing = lambda_.Tracing.DISABLED,
        memory_size: int = 128,
        source_code_directory: str,
        reserved_concurrent_executions: int | None = None,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            code=lambda_.Code.from_asset(
                path=f'../../runtime/functions/{source_code_directory}',
                bundling=cdk.BundlingOptions(
                    image=lambda_.Runtime.PYTHON_3_13.bundling_image,
                    command=['bash', '-c', 'rsync -r lambda_.py /asset-output'],
                ),
            ),
            handler='lambda_.handler',
            timeout=timeout,
            tracing=tracing,
            runtime=lambda_.Runtime.PYTHON_3_13,
            memory_size=memory_size,
            reserved_concurrent_executions=reserved_concurrent_executions,
            architecture=lambda_.Architecture.ARM_64,
        )


class Functions(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        data: Data,
        layers: Layers,
        project_name: str,
        sentry_dsn: str,
        sentry_environment: str,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
        )

        cdk.Aspects.of(self).add(
            cast(
                cdk.IAspect,
                ShareResources(
                    layers=layers,
                    project_name=project_name,
                    sentry_dsn=sentry_dsn,
                    sentry_environment=sentry_environment,
                ),
            )
        )