import aws_cdk as cdk
from constructs import Construct
from stack_constructs import (
    Data,
    Functions,
    HttpApi,
    Layers,
    Parameters,
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
        sentry_dsn: str,
        sentry_environment: str,
        http_api_name: str,
        http_api_domain_name: str,
        http_api_domain_zone_name: str,
        http_api_domain_record_name: str,
        http_api_domain_hosted_zone_id: str,
        http_api_domain_name_certificate_arn: str,
        param_http_api_cors_allow_origin: str,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
            stack_name=stack_name,
        )

        data = Data(
            self,
            'Data',
            project_name=project_name,
        )

        layers = Layers(
            self,
            'Layers',
        )

        Parameters(
            self,
            'Parameters',
            project_name=project_name,
            param_http_api_cors_allow_origin=param_http_api_cors_allow_origin,
        )

        functions = Functions(
            self,
            'Functions',
            data=data,
            layers=layers,
            project_name=project_name,
            sentry_dsn=sentry_dsn,
            sentry_environment=sentry_environment,
        )

        HttpApi(
            self,
            'HttpApi',
            http_api_name=http_api_name,
            http_api_function=functions.http_api,
            http_api_domain_name=http_api_domain_name,
            http_api_domain_zone_name=http_api_domain_zone_name,
            http_api_domain_record_name=http_api_domain_record_name,
            http_api_domain_hosted_zone_id=http_api_domain_hosted_zone_id,
            http_api_domain_name_certificate_arn=http_api_domain_name_certificate_arn,
        )

        cdk.Tags.of(self).add('project', project_name)
