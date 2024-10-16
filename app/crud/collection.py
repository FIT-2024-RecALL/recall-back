from sqlalchemy.orm import Session

from .. import models, schemas


def get_collection(db: Session, collection_id: int):
    return db.query(models.Collection).filter(models.Collection.id == collection_id).first()


def get_collections(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(models.Collection).offset(skip).limit(limit).all()


def create_user_collection(db: Session, collection: schemas.collection.CollectionCreate, user_id: int):
    db_collection = models.Collection(**collection.model_dump(),  owner_id=user_id)
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection
