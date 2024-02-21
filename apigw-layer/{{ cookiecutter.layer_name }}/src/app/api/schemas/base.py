__all__ = [
    'BaseModel',
]

from pydantic import BaseModel as PydanticBaseModel
from pydantic.alias_generators import to_camel


class BaseModel(PydanticBaseModel):
    model_config = {
        'extra': 'forbid',
        'from_attributes': True,
        'alias_generator': to_camel,
        'populate_by_name': True,
    }
