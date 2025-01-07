from typing import TYPE_CHECKING, Unpack, cast

if TYPE_CHECKING:
    from mypy_boto3_dynamodb.type_defs import QueryInputTableQueryTypeDef


def construct_query(
    **kwargs: Unpack['QueryInputTableQueryTypeDef'],
) -> 'QueryInputTableQueryTypeDef':
    new_kwargs = {key: value for key, value in kwargs.items() if value}
    return cast('QueryInputTableQueryTypeDef', new_kwargs)
