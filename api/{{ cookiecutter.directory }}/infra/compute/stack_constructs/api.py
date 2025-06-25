import json
from typing import cast

import aws_cdk as cdk
from aws_cdk import aws_apigatewayv2 as apigwv2
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
from constructs import Construct

from stack_constructs.functions import Functions


def get_routes(
    file_path: str,
    /,
) -> dict[str, dict[str, list[apigwv2.HttpMethod]]]:
    with open(file_path, 'r') as f:
        spec = json.load(f)

    routes = {}
    for path, methods in spec['paths'].items():
        segments = [s for s in path.split('/') if s]
        if not segments:
            continue

        resource = '/' + segments[0]
        sub_path = '/' + '/'.join(segments[1:]) if len(segments) > 1 else ''

        if resource not in routes:
            routes[resource] = {}

        routes[resource][sub_path] = [
            apigwv2.HttpMethod[method.upper()] for method in methods.keys()
        ]

    return routes


class LambdaIntegration(HttpLambdaIntegration):
    def _complete_bind(self, *, route: apigwv2.IHttpRoute, scope: Construct) -> None:
        return


class API(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        functions: Functions,
        api_domain_name: str,
        api_domain_zone_name: str,
        api_domain_record_name: str,
        api_domain_hosted_zone_id: str,
        api_domain_name_certificate_arn: str,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
        )

        certificate = acm.Certificate.from_certificate_arn(
            self,
            'Certificate',
            certificate_arn=api_domain_name_certificate_arn,
        )

        domain_name = apigwv2.DomainName(
            self,
            'DomainName',
            domain_name=api_domain_name,
            certificate=certificate,
        )

        api = apigwv2.HttpApi(
            self,
            'API',
            api_name=cdk.Names.unique_resource_name(self),
            create_default_stage=True,
            disable_execute_api_endpoint=True,
            default_domain_mapping=apigwv2.DomainMappingOptions(
                domain_name=domain_name,
            ),
        )

        integration = LambdaIntegration(
            'Integration',
            cast(
                lambda_.IFunction,
                functions.api,
            ),
        )

        # preflight
        api.add_routes(
            path='/{proxy+}',
            methods=[
                apigwv2.HttpMethod.OPTIONS,
            ],
            integration=integration,
        )

        routes = get_routes('openapi.json')
        for prefix in routes:
            for path, methods in routes[prefix].items():
                api.add_routes(
                    path=prefix + path,
                    methods=methods,
                    integration=integration,
                )

        source_arn = f'arn:{cdk.Aws.PARTITION}:execute-api:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:{api.api_id}/*'
        functions.api.add_permission(
            'APIPermissions',
            action='lambda:InvokeFunction',
            principal=cast(
                iam.IPrincipal,
                iam.ServicePrincipal('apigateway.amazonaws.com'),
            ),
            source_arn=source_arn,
        )

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            'HostedZone',
            zone_name=api_domain_zone_name,
            hosted_zone_id=api_domain_hosted_zone_id,
        )

        target = route53.RecordTarget.from_alias(
            alias_target=cast(
                route53.IAliasRecordTarget,
                targets.ApiGatewayv2DomainProperties(
                    regional_domain_name=domain_name.regional_domain_name,
                    regional_hosted_zone_id=domain_name.regional_hosted_zone_id,
                ),
            ),
        )

        route53.ARecord(
            self,
            'Record',
            zone=hosted_zone,
            record_name=api_domain_record_name,
            target=target,
        )
