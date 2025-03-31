from typing import Literal
from pydantic import BaseModel, ConfigDict

from .base import CamelCaseBaseModel

from app.core.minio import FileStream


__all__ = ["get_allowed_types", "get_allowed_exts", "FileCreate", "FileScheme", "StreamingFile"]


AllowedTypes = Literal["image", "video", "audio"]
AllowedExts = Literal[
    "bmp", "gif", "jpg", "jpeg", "png", "svg", "tif", "tiff", "webp",
    "avi", "m4v", "mkv", "mov", "mpg", "mp4", "ogv", "webm", "wmv",
    "aac", "flac", "m4a", "mp3", "oga", "ogg", "wav"
]

def get_allowed_types() -> list[str]:
    return list(AllowedTypes.__args__)

def get_allowed_exts() -> list[str]:
    return list(AllowedExts.__args__)

class FileCreate(CamelCaseBaseModel):
    owner_id: int
    filename: str
    type: AllowedTypes
    ext: AllowedExts


class FileScheme(FileCreate):
    id: int
    is_public: bool


class StreamingFile(BaseModel):
    """NOT FOR RESPONSES"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    metadata: FileScheme
    stream: FileStream
