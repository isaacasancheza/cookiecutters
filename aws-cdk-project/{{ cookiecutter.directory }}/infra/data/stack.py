import aws_cdk as cdk
from constructs import Construct
from stack_constructs import (
    Authentication,
    Database,
    Storage,
)


class Stack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        stack_name: str,
        project_name: str,
        removal_policy: cdk.RemovalPolicy,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            stack_name=stack_name,
        )

        Storage(
            self,
            'Storage',
            project_name=project_name,
            removal_policy=removal_policy,
        )

        Database(
            self,
            'Database',
            project_name=project_name,
            removal_policy=removal_policy,
        )

        Authentication(
            self,
            'Authentication',
            project_name=project_name,
            removal_policy=removal_policy,
        )

        cdk.Tags.of(self).add('project', project_name)
