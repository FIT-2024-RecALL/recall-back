from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_db_tables, close_db_connections
from app.routers import cards, collections, train_records, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    yield
    await close_db_connections()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(cards.router)
app.include_router(collections.router)
app.include_router(train_records.router)
app.include_router(users.router)
