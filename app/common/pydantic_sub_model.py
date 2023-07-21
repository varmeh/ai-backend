from pydantic import BaseModel
from ..util import snake_to_camel


class PydanticSubModel(BaseModel):
    class Config:
        alias_generator = snake_to_camel
        allow_population_by_field_name = True


__all__ = ["PydanticSubModel"]
