from pydantic import BaseModel
from ..util import to_camel_case


class PydanticSubModel(BaseModel):
    class Config:
        alias_generator = to_camel_case
        allow_population_by_field_name = True


__all__ = ["PydanticSubModel"]
