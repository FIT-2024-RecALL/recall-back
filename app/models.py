from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String(50), unique=True, index=True)
    password = Column(String(100))

    collections = relationship("Collection")


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100), index=True)
    description = Column(String, index=True)
