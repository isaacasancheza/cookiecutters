import aws_cdk as cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ssm as ssm
from constructs import Construct


class Bucket(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        name: str,
        project_name: str,
        removal_policy: cdk.RemovalPolicy,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
        )
        bucket = s3.Bucket(
            self,
            'Bucket',
            removal_policy=removal_policy,
            auto_delete_objects=removal_policy == cdk.RemovalPolicy.DESTROY,
        )
        ssm.StringParameter(
            self,
            'BucketName',
            string_value=bucket.bucket_name,
            parameter_name=f'/{project_name}/storage/{name}-bucket/name',
        )
        self.bucket = bucket


class Storage(Construct):
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
        main = Bucket(
            self,
            'Main',
            name='main',
            project_name=project_name,
            removal_policy=removal_policy,
        )
        self._main = main

    @property
    def main_bucket(self) -> s3.Bucket:
        return self._main.bucket
