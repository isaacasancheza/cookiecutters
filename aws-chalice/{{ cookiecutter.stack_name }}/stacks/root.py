import aws_cdk as cdk
from constructs import Construct

from stacks.chalice import ChaliceStack


class RootStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        chalice_stack: ChaliceStack = ChaliceStack(self, 'ChaliceStack')
