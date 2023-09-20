import aws_cdk as cdk
from constructs import Construct
from chalice.cdk import Chalice


class ChaliceStack(cdk.NestedStack):
    def __init__(self, scope: Construct, construct_id: str, source_dir: str = '/workspace/chalice') -> None:
        super().__init__(scope, construct_id)
        
        self.app: Chalice = Chalice(
            self, 
            'App', 
            source_dir=source_dir,
            stage_config={
                'environment_variables': {
                },
            },
        )
