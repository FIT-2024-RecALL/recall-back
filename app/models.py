from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.database import Base

"""
class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    train_record_id: Mapped[int] | None = mapped_column(ForeignKey("train_records.id"), )
    content: Mapped[str]
"""

class Collection(Base):
    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str] = mapped_column(index=True)


class TrainRecord(Base):
    __tablename__ = "train_records"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    meta_data: Mapped[str]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100))

    collections: Mapped[list[Collection]] = relationship("Collection")
    train_records: Mapped[list[TrainRecord]] = relationship("TrainRecord")

