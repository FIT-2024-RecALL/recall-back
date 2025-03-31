from pydantic import BaseModel, ConfigDict
from .base import CamelCaseBaseModel

from app.core.minio import FileStream


# __all__ = ["FileCreate", "FileScheme"]
__all__ = ["FileCreate", "FileScheme", "StreamingFile"]


class FileCreate(CamelCaseBaseModel):
    owner_id: int
    filename: str


class FileScheme(FileCreate):
    id: int
    is_public: bool


class StreamingFile(BaseModel):
    """NOT FOR RESPONSES"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    metadata: FileScheme
    stream: FileStream
