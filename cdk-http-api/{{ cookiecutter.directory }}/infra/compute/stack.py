import aws_cdk as cdk
from constructs import Construct
from stack_constructs import Data, Functions, Layers


class Stack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        stack_name: str,
        project_name: str,
        sentry_dsn: str,
        sentry_environment: str,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            stack_name=stack_name,
        )

        data = Data(
            self,
            'Data',
            project_name=project_name,
        )

        layers = Layers(
            self,
            'Layers',
        )

        Functions(
            self,
            'Functions',
            data=data,
            layers=layers,
            project_name=project_name,
            sentry_dsn=sentry_dsn,
            sentry_environment=sentry_environment,
        )

        cdk.Tags.of(self).add('project', project_name)
