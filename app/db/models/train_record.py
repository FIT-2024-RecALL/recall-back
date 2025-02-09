from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table, Numeric

from .metadata import get_metadata


__all__ = ["TrainRecordTable"]


TrainRecordTable = Table(
    "train_records", get_metadata(),
    Column("id", Integer, primary_key=True),
    Column("card_id", ForeignKey("cards.id", ondelete="CASCADE"), index=True, nullable=False),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
    Column("mark", Integer, nullable=False),
    Column("progress", Numeric(5, 4), nullable=False),
    Column("repeat_date", DateTime(timezone=True), nullable=False),
    Column("next_repeat_date", DateTime(timezone=True), nullable=False),
)
