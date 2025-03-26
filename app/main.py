from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import all_routers
from app.core import load_model
from app.db import close_db_connections, create_db_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_tables()
    print()
    print(await load_model())
    yield
    print(await load_model())
    print()
    await close_db_connections()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://letsrecall.ru', 'http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


for router in all_routers:
    app.include_router(router)


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
