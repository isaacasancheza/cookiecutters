from typing import cast

import aws_cdk as cdk
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_ssm as ssm
from constructs import Construct

from stack_constructs.storage import Storage


class CDN(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        storage: Storage,
        project_name: str,
    ) -> None:
        super().__init__(scope, construct_id)
        cache_policy = cloudfront.CachePolicy(
            self,
            'CachePolicy',
            min_ttl=cdk.Duration.days(365),
            max_ttl=cdk.Duration.days(365),
            default_ttl=cdk.Duration.days(365),
        )
        distribution = cloudfront.Distribution(
            self,
            'Distribution',
            price_class=cloudfront.PriceClass.PRICE_CLASS_100,
            default_behavior=cloudfront.BehaviorOptions(
                origin=cast(
                    cloudfront.IOrigin,
                    origins.S3BucketOrigin(
                        bucket=storage.cdn_bucket,
                    ),
                ),
                cache_policy=cache_policy,
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
        )
        ssm.StringParameter(
            self,
            'DomainName',
            string_value=distribution.domain_name,
            parameter_name=f'/{project_name}/cdn/domain-name',
        )
        self._distribution = distribution

    @property
    def domain_name(self) -> str:
        return self._distribution.domain_name
