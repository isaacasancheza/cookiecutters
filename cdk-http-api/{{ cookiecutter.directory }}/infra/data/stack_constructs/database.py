import aws_cdk as cdk
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_ssm as ssm
from constructs import Construct


class Main(Construct):
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
        table = dynamodb.TableV2(
            self,
            'Table',
            billing=dynamodb.Billing.on_demand(),
            removal_policy=removal_policy,
            partition_key=dynamodb.Attribute(
                name='pk',
                type=dynamodb.AttributeType.STRING,
            ),
            sort_key=dynamodb.Attribute(
                name='sk',
                type=dynamodb.AttributeType.STRING,
            ),
            time_to_live_attribute='ttl',
        )
        ssm.StringParameter(
            self,
            'TableName',
            string_value=table.table_name,
            parameter_name=f'/{project_name}/database/main-table/name',
        )
        self.table = table
        self._add_global_secondary_indexes()

    def _add_global_secondary_indexes(self) -> None:
        pass


class Database(Construct):
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
        main = Main(
            self,
            'Main',
            project_name=project_name,
            removal_policy=removal_policy,
        )

        self._main = main

    @property
    def main_table(self) -> dynamodb.TableV2:
        return self._main.table
