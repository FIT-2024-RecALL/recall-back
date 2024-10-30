from sqlalchemy import Column, ForeignKey, Integer, String, Table

from app.database import metadata


UserTable = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(100), unique=True, nullable=False),
    Column("nickname", String(50), unique=True, nullable=False),
    Column("hashed_password", String(1024), nullable=False)
) ### Есть связь с collections и train_records


CardTable = Table(
    "cards",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("content", String, nullable=False)
) ### Есть связь с collections и train_records


CollectionTable = Table(
    "collections",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("owner_id", ForeignKey("users.id"), nullable=False),
    Column("title", String(100), nullable=False),
    Column("description", String, nullable=True)
) ### Есть связь с cards


CardCollectionTable = Table(
    "card_collection",
    metadata,
    Column("card_id", ForeignKey("cards.id"), primary_key=True),
    Column("collection_id", ForeignKey("collections.id"), primary_key=True)
)


TrainRecordTable = Table(
    "train_records",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("card_id", ForeignKey("cards.id"), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("meta_data", String, nullable=True)
)
