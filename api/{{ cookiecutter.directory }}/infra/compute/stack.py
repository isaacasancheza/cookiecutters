import aws_cdk as cdk
from constructs import Construct
from stack_constructs.api import API
from stack_constructs.data import Data
from stack_constructs.functions import Functions
from stack_constructs.layers import Layers
from stack_constructs.parameters import Parameters


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
        api_domain_name: str,
        api_domain_zone_name: str,
        api_domain_record_name: str,
        api_domain_hosted_zone_id: str,
        api_domain_name_certificate_arn: str,
        param_api_cors_allow_origin: str,
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
            param_api_cors_allow_origin=param_api_cors_allow_origin,
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
        API(
            self,
            'API',
            functions=functions,
            api_domain_name=api_domain_name,
            api_domain_zone_name=api_domain_zone_name,
            api_domain_record_name=api_domain_record_name,
            api_domain_hosted_zone_id=api_domain_hosted_zone_id,
            api_domain_name_certificate_arn=api_domain_name_certificate_arn,
        )
        cdk.Tags.of(self).add('project', project_name)
