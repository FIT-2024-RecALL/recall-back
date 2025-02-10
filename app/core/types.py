from pydantic import BaseModel
from typing import TypeVar


__all__ = ["SchemaType"]


SchemaType = TypeVar("SchemaType", bound=BaseModel)
