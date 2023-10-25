import aws_cdk as cdk
from constructs import Construct
from chalice.cdk import Chalice


class ChaliceNestedStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, /, *, source_dir: str = 'chalice') -> None:
        super().__init__(scope, construct_id)
        
        self.app = Chalice(
            self, 
            'App', 
            source_dir=source_dir,
        )
