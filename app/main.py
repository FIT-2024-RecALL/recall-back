from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.db import close_db_connections, create_db_tables
from app.api import cards, collections, storage, train_records, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    yield
    await close_db_connections()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://letsrecall.ru', 'http://localhost:5173'],
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

@app.get("/items/{item_id}", responses={
    status.HTTP_404_NOT_FOUND: {"description": "Item not found"},
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal Server Error"},
})
async def read_item(item_id: int | None = None):
    return {"item_id": item_id}
############################
### БУДЕТ УДАЛЕН ПОЗДНЕЕ ###
############################


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
