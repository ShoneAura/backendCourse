from pydantic import BaseModel
from typing import TypeVar, Type

from src.models.base import Base

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: Type[Base] = None
    schema: Type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.db_model(**data.model_dump())
