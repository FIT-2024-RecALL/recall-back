from fastapi import FastAPI

from app import models
from app.database import engine
from app.routers import collections, train_records, users

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(collections.router)
app.include_router(train_records.router)
app.include_router(users.router)
