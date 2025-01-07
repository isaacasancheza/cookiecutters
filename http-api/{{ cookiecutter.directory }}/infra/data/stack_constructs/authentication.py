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
            email=None,
            auto_verify=None,
            sign_in_aliases=cognito.SignInAliases(
                username=True,
            ),
            account_recovery=None,
            user_verification=None,
            standard_attributes=None,
            self_sign_up_enabled=True,
        )
        user_pool_client = user_pool.add_client(
            'UserPoolClient',
            auth_flows=cognito.AuthFlow(
                user_password=True,
            ),
            access_token_validity=cdk.Duration.days(1),
            refresh_token_validity=cdk.Duration.days(30),
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
