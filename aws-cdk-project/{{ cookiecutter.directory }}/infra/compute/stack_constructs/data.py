from aws_cdk import aws_cognito as cognito
from aws_cdk import aws_dynamodb as dynamodb
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
    ) -> None:
        super().__init__(scope, construct_id)
        bucket_name = ssm.StringParameter.from_string_parameter_attributes(
            self,
            'Name',
            parameter_name=f'/{project_name}/storage/{name}-bucket/name',
        )
        bucket = s3.Bucket.from_bucket_name(
            self,
            'Bucket',
            bucket_name=bucket_name.string_value,
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
    ) -> None:
        super().__init__(scope, construct_id)
        main = Bucket(
            self,
            'Main',
            name='main',
            project_name=project_name,
        )
        self._main = main

    @property
    def main_bucket(self) -> s3.IBucket:
        return self._main.bucket


class Table(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        name: str,
        project_name: str,
    ) -> None:
        super().__init__(scope, construct_id)
        table_name = ssm.StringParameter.from_string_parameter_attributes(
            self,
            'Name',
            parameter_name=f'/{project_name}/database/{name}-table/name',
        )
        table = dynamodb.TableV2.from_table_attributes(
            self,
            'Table',
            table_name=table_name.string_value,
            grant_index_permissions=True,
        )
        self.table = table


class Database(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        project_name: str,
    ) -> None:
        super().__init__(scope, construct_id)
        main = Table(
            self,
            'Main',
            name='main',
            project_name=project_name,
        )
        self._main = main

    @property
    def main_table(self) -> dynamodb.ITableV2:
        return self._main.table


class Authentication(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        project_name: str,
    ) -> None:
        super().__init__(
            scope,
            construct_id,
        )
        user_pool_id = ssm.StringParameter.from_string_parameter_attributes(
            self,
            'UserPoolId',
            parameter_name=f'/{project_name}/authentication/user-pool/id',
        )
        user_pool = cognito.UserPool.from_user_pool_id(
            self,
            'UserPool',
            user_pool_id=user_pool_id.string_value,
        )
        user_pool_client_id = ssm.StringParameter.from_string_parameter_attributes(
            self,
            'UserPoolClientId',
            parameter_name=f'/{project_name}/authentication/user-pool-client/id',
        )
        user_pool_client = cognito.UserPoolClient.from_user_pool_client_id(
            self,
            'UserPoolClient',
            user_pool_client_id=user_pool_client_id.string_value,
        )
        self.user_pool = user_pool
        self.user_pool_client = user_pool_client


class Data(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        /,
        *,
        project_name: str,
    ) -> None:
        super().__init__(scope, construct_id)
        storage = Storage(
            self,
            'Storage',
            project_name=project_name,
        )
        database = Database(
            self,
            'Database',
            project_name=project_name,
        )
        authentication = Authentication(
            self,
            'Authentication',
            project_name=project_name,
        )
        self.storage = storage
        self.database = database
        self.authentication = authentication
