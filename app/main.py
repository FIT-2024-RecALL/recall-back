from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine
from app.routers import users #, cards, collections, train_records


models.metadata.create_all(bind=engine)

app = FastAPI()


#app.include_router(cards.router)
#app.include_router(collections.router)
#app.include_router(train_records.router)
app.include_router(users.router)
