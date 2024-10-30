from sqlalchemy import Connection, select, insert, exists, or_

from app import models, schemas


def get_card(conn: Connection, card_id: int):
    query = select(models.CardTable.c[*schemas.card.Card.model_fields]).where(
        models.CardTable.c.id == card_id
    )
    return conn.execute(query).mappings().first()


def get_cards(conn: Connection, *, limit: int, skip: int):
    query = select(models.CardTable.c[*schemas.card.Card.model_fields]).limit(limit).offset(skip)
    return conn.execute(query).mappings().all()


def create_card(conn: Connection, card: schemas.card.CardCreate):
    query = insert(models.CardTable).values(**card.model_dump()).returning(
        models.CardTable.c[*schemas.card.Card.model_fields]
    )
    result = conn.execute(query).mappings().first()
    conn.commit()
    return result
