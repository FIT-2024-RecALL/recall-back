from sqlalchemy.orm import Session

from app import models, schemas


def get_train_record(db: Session, train_record_id: int):
    return db.query(models.TrainRecord).filter(models.TrainRecord.id == train_record_id).first()


def get_train_records(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(models.TrainRecord).offset(skip).limit(limit).all()


def create_train_record(
        db: Session, train_record: schemas.train_record.TrainRecordCreate, card_id: int, user_id: int
):
    db_train_record = models.TrainRecord(**train_record.model_dump(), card_id=card_id, user_id=user_id)
    db.add(db_train_record)
    db.commit()
    db.refresh(db_train_record)
    return db_train_record
