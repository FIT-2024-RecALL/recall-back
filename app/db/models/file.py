from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table
from sqlalchemy.dialects.postgresql import ENUM

from .metadata import get_metadata
from app.schemas import get_allowed_types, get_allowed_exts


__all__ = ["FileTable"]


file_types = ENUM(*get_allowed_types(), name="file_types", metadata=get_metadata())
file_exts = ENUM(*get_allowed_exts(), name="file_exts", metadata=get_metadata())


FileTable = Table(
    "files", get_metadata(),
    Column("id", Integer, primary_key=True),
    Column("owner_id", ForeignKey("users.id"), index=True, nullable=False),
    Column("filename", String, index=True, nullable=False, unique=True),
    Column("type", file_types, nullable=False),
    Column("ext", file_exts, nullable=False),
    Column("size", Integer, nullable=True, default=None),
    Column("is_public", Boolean, nullable=False, default=False)
)
