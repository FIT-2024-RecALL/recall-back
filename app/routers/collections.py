from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix="/collections",
    tags=["collection"]
)


@router.get("/{collection_id}", response_model=schemas.collection.Collection)
def read_collection(collection_id: int, db: Session = Depends(get_db)):
    db_collection = crud.collection.get_collection(db, collection_id=collection_id)
    if db_collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return db_collection


@router.get("/{collection_id}/cards", response_model=list[schemas.card.Card])
def read_collection_cards(collection_id: int, db: Session = Depends(get_db)):
    return read_collection(collection_id, db).cards


@router.get("/", response_model=list[schemas.collection.Collection])
def read_collections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.collection.get_collections(db, skip=skip, limit=limit)


@router.post("/{user_id}", response_model=schemas.collection.Collection)
def create_collection(
        user_id: int, collection: schemas.collection.CollectionCreate, db: Session = Depends(get_db)
):
    db_user = crud.user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User with this id doesn't exist")
    return crud.collection.create_collection(db=db, collection=collection, user_id=user_id)


"""
@router.post("/{collection_id}/pair")
def update_card_collection_connection(collection_id: int, db: Session = Depends(get_db)):
    statement = insert(models.association_table).values(card_id=card_id, collection_id=collection_id)
    db.execute(statement)
    db.commit()
"""