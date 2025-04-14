from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table

from .metadata import get_metadata


__all__ = ["CollectionTable"]


CollectionTable = Table(
    "collections", get_metadata(),
    Column("id", Integer, primary_key=True),
    Column("owner_id", ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
    Column("title", String(100), index=True, nullable=False),
    Column("description", String, nullable=True),
    Column("is_public", Boolean, nullable=False, default=False)
)
