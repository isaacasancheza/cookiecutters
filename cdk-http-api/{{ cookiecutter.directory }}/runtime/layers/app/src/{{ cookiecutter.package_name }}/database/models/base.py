from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    model_config = {
        'use_enum_values': True,
        'from_attributes': True,
    }

    def dump(self):
        return self.model_dump(
            mode='json',
            exclude_none=True,
        )
