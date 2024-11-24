from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import create_db_tables, close_db_connections
from app.routers import cards, collections, train_records, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    yield
    await close_db_connections()

app = FastAPI(lifespan=lifespan)


app.include_router(cards.router)
app.include_router(collections.router)
app.include_router(train_records.router)
app.include_router(users.router)
