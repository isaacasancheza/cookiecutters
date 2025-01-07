from typing import Generic, TypeVar

from app.api.schemas.base import BaseModel

Model = TypeVar('Model', bound='BaseModel')


class Connection(BaseModel, Generic[Model]):
    nodes: list[Model]
