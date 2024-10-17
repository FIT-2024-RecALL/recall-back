from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base


association_table = Table(
    "association_table",
    Base.metadata,
    Column("card_id", ForeignKey("cards.id"), primary_key=True),
    Column("collection_id", ForeignKey("collections.id"), primary_key=True),
)


class TrainRecord(Base):
    __tablename__ = "train_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    meta_data: Mapped[str]


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]

    collections: Mapped[list["Collection"]] = relationship(
        secondary=association_table, back_populates="cards"
    )
    train_records: Mapped[list[TrainRecord]] = relationship("TrainRecord")


class Collection(Base):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(index=True)

    cards: Mapped[list["Card"]] = relationship(
        secondary=association_table, back_populates="collections"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100))

    collections: Mapped[list[Collection]] = relationship("Collection")
    train_records: Mapped[list[TrainRecord]] = relationship("TrainRecord")

