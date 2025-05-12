from functools import cache
from typing import Literal, get_args
from pydantic import BaseModel, ConfigDict

from .base import CamelCaseBaseModel, PublicStatusMixin
from app.core.minio import FileStream

__all__ = ["get_allowed_types", "get_allowed_exts", "FileCreate", "FileMeta", "StreamingFile"]


AllowedTypes = Literal["image", "video", "audio"]
AllowedExts = Literal[
    "bmp", "gif", "jpg", "jpeg", "png", "svg", "tif", "tiff", "webp",
    "avi", "m4v", "mkv", "mov", "mpg", "mp4", "ogv", "webm", "wmv",
    "aac", "flac", "m4a", "mp3", "mpeg", "oga", "ogg", "wav"
]


@cache
def get_allowed_types() -> list[str]:
    """Возвращает список допустимых типов файлов."""
    return list(get_args(AllowedTypes))


@cache
def get_allowed_exts() -> list[str]:
    """Возвращает список допустимых расширений файлов."""
    return list(get_args(AllowedExts))


class FileCreate(CamelCaseBaseModel):
    owner_id: int
    filename: str
    type: AllowedTypes
    ext: AllowedExts


class FileMeta(FileCreate, PublicStatusMixin):
    pass


class StreamingFile(BaseModel):
    """Модель для потоковой передачи файла с метаданными. Не используется в ответах API."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    metadata: FileMeta
    stream: FileStream
