from typing import TYPE_CHECKING, Unpack, cast

from boto3.dynamodb.conditions import Attr, Key

from app import constants
from app.database.tables import main_table

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.type_defs import QueryInputTableQueryTypeDef


def construct_query(
    **kwargs: Unpack['QueryInputTableQueryTypeDef'],
) -> 'QueryInputTableQueryTypeDef':
    new_kwargs = {key: value for key, value in kwargs.items() if value}
    return cast('QueryInputTableQueryTypeDef', new_kwargs)


def check_if_slug_exists(
    *,
    slug: str,
    sort_key: constants.KeyPrefix,
    partition_key: str,
) -> bool:
    """Returns True of False if slug exists."""
    count = main_table.query(
        Select='COUNT',
        ConsistentRead=True,
        FilterExpression=Attr('slug').eq(slug),
        KeyConditionExpression=Key('pk').eq(partition_key)
        & Key('sk').begins_with(sort_key),
    )['Count']
    return count > 0
