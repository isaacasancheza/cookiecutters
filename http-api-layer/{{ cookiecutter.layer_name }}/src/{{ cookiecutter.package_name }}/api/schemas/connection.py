from typing import Generic, TypeVar

from app.api.schemas.base import BaseModel
from app.types.composite_keys import CompositeKey

Model = TypeVar('Model', bound='BaseModel')


class Connection(BaseModel, Generic[Model]):
    nodes: list[Model]
    cursor: CompositeKey | tuple[str, str] | None = None
