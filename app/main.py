from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .database import create_db_tables, close_db_connections
from app.routers import cards, collections, train_records, users, storage


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
app.include_router(storage.router)


###################################################
### ВРЕМЕННЫЙ КОД, КОТОРЫЙ БУДЕТ УДАЛЕН ПОЗДНЕЕ ###
###################################################
from fastapi import status
from app.helpers.dependencies import DBConnection
from app.schemas import Card, TrainRecord, User, Collection
from app import crud

@app.get("/items/{item_id}", responses={
    status.HTTP_404_NOT_FOUND: {"description": "Item not found"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
})
async def read_item(item_id: int | None = None):
    return {"item_id": item_id}

@app.get("/admin/cards", response_model=list[Card])
async def read_cards(conn: DBConnection, skip: int = 0, limit: int | None = None):
    return await crud.get_cards(conn, limit=limit, skip=skip)

@app.get("/admin/train_records", response_model=list[TrainRecord])
async def read_train_records(conn: DBConnection, skip: int = 0, limit: int | None = None):
    return await crud.get_train_records(conn, skip=skip, limit=limit)

@app.get("/admin/users", response_model=list[User])
async def read_users(conn: DBConnection, limit: int = 100, skip: int = 0):
    return await crud.get_users(conn, limit=limit, skip=skip)

@app.get("/admin/collections", response_model=list[Collection])
async def read_collections(conn: DBConnection, skip: int = 0, limit: int | None = None):
    return await crud.get_collections(conn, limit=limit, skip=skip)
############################
### БУДЕТ УДАЛЕН ПОЗДНЕЕ ###
############################


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
