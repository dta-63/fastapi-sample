from typing import Any, Optional, Generic, TypeVar, List
from bson import ObjectId
from pydantic import BaseModel
from pydantic.generics import GenericModel


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(str(v)):
            return ValueError(f"Not a valid ObjectId: {v}")
        return ObjectId(str(v))


class DBModelMixin(BaseModel):
    id: Optional[ObjectIdStr]

    def __init__(self, **data: Any):
        if '_id' in data:
            data['id'] = data.pop('_id')
        super().__init__(**data)

    class Config:
        json_encoders = {ObjectId: lambda x: str(x)}


T = TypeVar('T')


class Pagination(GenericModel, Generic[T]):
    """
    Pagination model
    Wrap a generic list of items with skip, limit and counter
    """
    limit: int = 10
    skip: int = 0
    count: int = 0
    items: List[T] = []

    class Config:
        json_encoders = {ObjectId: lambda x: str(x)}