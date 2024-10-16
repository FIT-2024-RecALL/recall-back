from sqlalchemy.orm import Session

from app import models, schemas


def get_card(db: Session, card_id: int):
    return db.query(models.Card).filter(models.Card.id == card_id).first()


def get_cards(db: Session, *, skip: int = 0, limit: int = 100):
    return db.query(models.Card).offset(skip).limit(limit).all()


def create_card(db: Session, card: schemas.card.CardCreate, train_record_id: int | None):
    db_card = models.Card(**card.model_dump(), train_record_id=train_record_id)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card
