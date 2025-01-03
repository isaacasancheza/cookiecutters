from datetime import datetime, timezone

from pydantic import BaseModel as PydanticBaseModel
from pydantic import PrivateAttr
from pydantic.alias_generators import to_camel


class BaseModel(PydanticBaseModel):
    model_config = {
        'extra': 'forbid',
        'alias_generator': to_camel,
        'use_enum_values': True,
        'from_attributes': True,
        'populate_by_name': True,
    }
    _created_at: datetime = PrivateAttr(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    _updated_at: datetime = PrivateAttr(
        default_factory=lambda: datetime.now(timezone.utc)
    )
