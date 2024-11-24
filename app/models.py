from sqlalchemy import Column, ForeignKey, Integer, String, Table, MetaData

__all__ = [
    "UserTable", "CardTable", "CollectionTable", "CardCollectionTable", "TrainRecordTable"
]


_metadata = MetaData()


UserTable = Table(
    "users",
    _metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(100), unique=True, nullable=False),
    Column("nickname", String(50), unique=True, nullable=False),
    Column("hashed_password", String(1024), nullable=False)
) ### Есть связь с collections и train_records


CardTable = Table(
    "cards",
    _metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", ForeignKey("users.id"), nullable=False),
    Column("front_side", String, nullable=False),
    Column("back_side", String, nullable=False)
) ### Есть связь с collections и train_records


CollectionTable = Table(
    "collections",
    _metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", ForeignKey("users.id"), nullable=False),
    Column("title", String(100), nullable=False),
    Column("description", String, nullable=True)
) ### Есть связь с cards


CardCollectionTable = Table(
    "card_collection",
    _metadata,
    Column("card_id", ForeignKey("cards.id"), primary_key=True),
    Column("collection_id", ForeignKey("collections.id"), primary_key=True)
)


TrainRecordTable = Table(
    "train_records",
    _metadata,
    Column("id", Integer, primary_key=True),
    Column("card_id", ForeignKey("cards.id"), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("meta_data", String, nullable=True)
)
