from fastapi import FastAPI

from app.database import create_tables, close_connections
from app.routers import cards, collections, train_records, users

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await close_connections()

app = FastAPI(lifespan=lifespan)


app.include_router(cards.router)
app.include_router(collections.router)
app.include_router(train_records.router)
app.include_router(users.router)
