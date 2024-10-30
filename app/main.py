from fastapi import FastAPI


from app import models
from app.database import engine
from app.routers import cards, collections, users#, train_records


models.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(cards.router)
app.include_router(collections.router)
#app.include_router(train_records.router)
app.include_router(users.router)
