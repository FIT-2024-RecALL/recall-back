from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table

from .metadata import get_metadata


__all__ = ["FileTable"]


FileTable = Table(
    "files", get_metadata(),
    Column("id", Integer, primary_key=True),
    Column("owner_id", ForeignKey("users.id"), index=True, nullable=False),
    Column("filename", String, index=True, nullable=False, unique=True),
    Column("is_public", Boolean, nullable=False, default=False)
)
