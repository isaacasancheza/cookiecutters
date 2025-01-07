from aws_cdk import aws_ssm as ssm
from constructs import Construct


class HttpApi(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        project_name: str,
        param_http_api_cors_allow_origin: str,
    ) -> None:
        super().__init__(scope, construct_id)
        ssm.StringParameter(
            self,
            'CorsAllowOrigin',
            string_value=param_http_api_cors_allow_origin,
            parameter_name=f'/{project_name}/http-api/cors-allow-origin',
        )
        self.cors_allow_origin = param_http_api_cors_allow_origin


class Parameters(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        project_name: str,
        param_http_api_cors_allow_origin: str,
    ) -> None:
        super().__init__(scope, construct_id)
        http_api = HttpApi(
            self,
            'HttpApi',
            project_name=project_name,
            param_http_api_cors_allow_origin=param_http_api_cors_allow_origin,
        )
        self.http_api = http_api
