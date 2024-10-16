from fastapi import FastAPI, Depends
from sqlalchemy import insert
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_db
from app.routers import cards, collections, train_records, users


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(cards.router)
app.include_router(collections.router)
app.include_router(train_records.router)
app.include_router(users.router)


@app.put("/root/{card_id}/{collection_id}", tags=["root"])
def update_card_collection_connection(card_id: int, collection_id: int, db: Session = Depends(get_db)):
    statement = insert(models.association_table).values(card_id=card_id, collection_id=collection_id)
    db.execute(statement)
    db.commit()
