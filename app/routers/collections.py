from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix="/collections",
    tags=["collection"]
)


@router.get("/", response_model=list[schemas.collection.Collection])
def read_collections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    collections = crud.collection.get_collections(db, skip=skip, limit=limit)
    return collections


@router.get("/{collection_id}", response_model=schemas.collection.Collection)
def read_collection(collection_id: int, db: Session = Depends(get_db)):
    db_collection = crud.collection.get_collection(db, collection_id=collection_id)
    if db_collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return db_collection
