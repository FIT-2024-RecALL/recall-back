from sqlalchemy.orm import Session

from .. import models, schemas


def get_train_record(db: Session, train_record_id: int):
    return db.query(models.TrainRecord).filter(models.TrainRecord.id == train_record_id).first()


def get_train_records(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(models.TrainRecord).offset(skip).limit(limit).all()


def create_user_train_record(db: Session, train_record: schemas.train_record.TrainRecordCreate, user_id: int):
    db_train_record = models.TrainRecord(**train_record.model_dump(), user_id=user_id)
    db.add(db_train_record)
    db.commit()
    db.refresh(db_train_record)
    return db_train_record
