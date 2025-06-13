from aws_cdk import aws_ssm as ssm
from constructs import Construct


class Api(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        project_name: str,
        param_api_cors_allow_origin: str,
    ) -> None:
        super().__init__(scope, construct_id)
        ssm.StringParameter(
            self,
            'CorsAllowOrigin',
            string_value=param_api_cors_allow_origin,
            parameter_name=f'/{project_name}/api/cors-allow-origin',
        )
        self.cors_allow_origin = param_api_cors_allow_origin


class Parameters(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        project_name: str,
        param_api_cors_allow_origin: str,
    ) -> None:
        super().__init__(scope, construct_id)
        api = Api(
            self,
            'Api',
            project_name=project_name,
            param_api_cors_allow_origin=param_api_cors_allow_origin,
        )
        self.api = api
