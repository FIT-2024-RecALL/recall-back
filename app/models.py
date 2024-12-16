from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, MetaData, Numeric

__all__ = [
    "UserTable", "CardTable", "CollectionTable", "CardCollectionTable", "TrainRecordTable"
]


_metadata = MetaData()


UserTable = Table(
    "users",
    _metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(100), unique=True, index=True, nullable=False),
    Column("nickname", String(35), unique=True, index=True, nullable=False),
    Column("hashed_password", String(1024), nullable=False)
)


CardTable = Table(
    "cards",
    _metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
    Column("front_side", String, nullable=False),
    Column("back_side", String, nullable=False)
)


CollectionTable = Table(
    "collections",
    _metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
    Column("title", String(100), index=True, nullable=False),
    Column("description", String, nullable=True)
)


CardCollectionTable = Table(
    "card_collection",
    _metadata,
    Column("card_id", ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True),
    Column("collection_id", ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True)
)


TrainRecordTable = Table(
    "train_records",
    _metadata,
    Column("id", Integer, primary_key=True),
    Column("card_id", ForeignKey("cards.id", ondelete="CASCADE"), index=True, nullable=False),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
    Column("mark", Integer, nullable=False),
    Column("progress", Numeric(5, 4), nullable=False),
    Column("repeat_date", DateTime(timezone=True), nullable=False),
    Column("next_repeat_date", DateTime(timezone=True), nullable=False),
)
