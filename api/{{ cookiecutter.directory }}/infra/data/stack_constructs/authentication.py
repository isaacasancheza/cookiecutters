import aws_cdk as cdk
from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_ssm as ssm
from constructs import Construct


class Authentication(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        project_name: str,
        removal_policy: cdk.RemovalPolicy,
    ) -> None:
        super().__init__(scope, construct_id)
        user_pool = cognito.UserPool(
            self,
            'UserPool',
            removal_policy=removal_policy,
        )
        user_pool_client = user_pool.add_client(
            'UserPoolClient',
        )
        ssm.StringParameter(
            self,
            'UserPoolId',
            string_value=user_pool.user_pool_id,
            parameter_name=f'/{project_name}/authentication/user-pool/id',
        )
        ssm.StringParameter(
            self,
            'UserPoolRegion',
            string_value=cdk.Aws.REGION,
            parameter_name=f'/{project_name}/authentication/user-pool/region',
        )
        ssm.StringParameter(
            self,
            'UserPoolClientId',
            string_value=user_pool_client.user_pool_client_id,
            parameter_name=f'/{project_name}/authentication/user-pool-client/id',
        )
        self.user_pool = user_pool
        self.user_pool_client = user_pool_client
