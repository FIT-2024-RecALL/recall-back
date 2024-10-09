from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_collection(db: Session, collection_id: int):
    return db.query(models.Collection).filter(models.Collection.id == collection_id).first()


def get_collections(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(models.Collection).offset(skip).limit(limit).all()


def create_user_collection(db: Session, collection: schemas.CollectionCreate, user_id: int):
    db_collection = models.Collection(**collection.model_dump(),  owner_id=user_id)
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection
