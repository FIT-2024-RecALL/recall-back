from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["user"]
)


@router.post("/", response_model=schemas.user.User)
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user_email = crud.user.get_user_by_email(db, email=user.email)
    db_user_name = crud.user.get_user_by_name(db, name=user.name)
    if db_user_email or db_user_name:
        raise HTTPException(status_code=400, detail="Email or Name already registered")
    return crud.user.create_user(db=db, user=user)



@router.get("/", response_model=list[schemas.user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.user.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/train_records/", response_model=schemas.train_record.TrainRecord, tags=["train_record"])
def create_train_record_for_user(
        user_id: int, train_record: schemas.train_record.TrainRecordCreate, db: Session = Depends(get_db)
):
    db_user = crud.user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User with this id doesn't exist")
    return crud.train_record.create_user_train_record(db=db, train_record=train_record, user_id=user_id)


@router.post("/{user_id}/collections/", response_model=schemas.collection.Collection, tags=["collection"])
def create_collection_for_user(
        user_id: int, collection: schemas.collection.CollectionCreate, db: Session = Depends(get_db)
):
    db_user = crud.user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User with this id doesn't exist")
    return crud.collection.create_user_collection(db=db, collection=collection, user_id=user_id)
