from sqlalchemy import Column, ForeignKey, Table

from .metadata import get_metadata


__all__ = ["CardCollectionTable"]


CardCollectionTable = Table(
    "card_collection", get_metadata(),
    Column("card_id", ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True),
    Column("collection_id", ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True)
)
