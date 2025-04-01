from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table

from .metadata import get_metadata


__all__ = ["CardTable"]


CardTable = Table(
    "cards", get_metadata(),
    Column("id", Integer, primary_key=True),
    Column("owner_id", ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
    Column("front_side", String, nullable=False),
    Column("back_side", String, nullable=False),
    Column("is_public", Boolean, nullable=False, default=False)
)
