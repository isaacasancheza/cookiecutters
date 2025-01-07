from abc import ABC
from datetime import datetime

from app import constants, utils
from app.database.models.base import BaseModel
from pydantic import PrivateAttr


class Image(ABC, BaseModel):
    url: str
    width: int
    height: int
    format: str
    extension: str
    content_type: str
    created_at: datetime

    _sk: str = PrivateAttr(
        default_factory=lambda: utils.generate_sk(constants.KeyPrefix.IMAGE)
    )

    @property
    def pk(self) -> str:
        pk, _ = getattr(self, 'id')
        return pk

    @property
    def sk(self) -> str:
        _, sk = getattr(self, 'id')
        return sk
