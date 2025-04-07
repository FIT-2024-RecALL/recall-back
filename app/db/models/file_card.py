from sqlalchemy import Column, ForeignKey, Table

from .metadata import get_metadata


__all__ = ["FileCardTable"]


FileCardTable = Table(
    "file_card", get_metadata(),
    Column("file_id", ForeignKey("files.id", ondelete="CASCADE"), primary_key=True),
    Column("card_id", ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True)
)
