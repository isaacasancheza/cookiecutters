import aws_cdk as cdk
from constructs import Construct

from nested_stacks.chalice import ChaliceNestedStack


class Stack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        chalice_stack: ChaliceNestedStack = ChaliceNestedStack(
            self,
            'ChaliceNestedStack',
        )    
