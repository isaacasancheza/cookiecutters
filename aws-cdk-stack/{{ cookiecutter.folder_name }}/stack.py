import aws_cdk as cdk
from constructs import Construct


class Stack(cdk.Stack):
    def __init__(
            self, 
            scope: Construct, 
            construct_id: str, 
            /,
            *,
            stack_name: str,
            project_name: str,
        ) -> None:
        super().__init__(
            scope, 
            construct_id,
            stack_name=stack_name,
        )

        cdk.Tags.of(self).add('project', project_name)
