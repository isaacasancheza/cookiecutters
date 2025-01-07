from abc import ABC
from datetime import datetime, timezone
from typing import cast

from pydantic import Field

from app import constants, settings, types, utils
from app.database.models.base import BaseModel


class Image(BaseModel, ABC):
    sk: types.ImageSk = Field(
        default_factory=lambda: utils.generate_sk(constants.KeyPrefix.IMAGE)
    )

    width: int
    height: int
    format: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def extension(self):
        return self.format

    @property
    def content_type(self):
        return f'image/{self.format}'

    @property
    def id(self):
        pk = getattr(self, 'pk')
        sk = getattr(self, 'sk')
        return cast(str, pk), cast(str, sk)

    @property
    def encoded_id(self):
        return utils.encode_tuple(self.id)

    @property
    def key(self):
        return f'images/{self.encoded_id}.{self.extension}'

    @property
    def url(self):
        return f'https://{settings.CDN_DOMAIN_NAME}/{self.key}'

    @property
    def bucket(self):
        return settings.CDN_BUCKET_NAME
