from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User, tags=["user"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_email = crud.get_user_by_email(db, email=user.email)
    db_user_name = crud.get_user_by_name(db, name=user.name)
    if db_user_email or db_user_name:
        raise HTTPException(status_code=400, detail="Email or Name already registered")
    return crud.create_user(db=db, user=user)



@app.get("/users/", response_model=list[schemas.User], tags=["user"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User, tags=["user"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/train_records/", response_model=schemas.TrainRecord, tags=["train_record"])
def create_train_record_for_user(
        user_id: int, train_record: schemas.TrainRecordCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User with this id doesn't exist")
    return crud.create_user_train_record(db=db, train_record=train_record, user_id=user_id)


@app.get("/train_records/", response_model=list[schemas.TrainRecord], tags=["train_record"])
def read_train_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    train_records = crud.get_train_records(db, skip=skip, limit=limit)
    return train_records


@app.get("/train_records/{train_record_id}", response_model=schemas.TrainRecord, tags=["train_record"])
def read_train_record(train_record_id: int, db: Session = Depends(get_db)):
    db_train_record = crud.get_train_record(db, train_record_id=train_record_id)
    if db_train_record is None:
        raise HTTPException(status_code=404, detail="TrainRecord not found")
    return db_train_record


@app.post("/users/{user_id}/collections/", response_model=schemas.Collection, tags=["collection"])
def create_collection_for_user(
        user_id: int, collection: schemas.CollectionCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User with this id doesn't exist")
    return crud.create_user_collection(db=db, collection=collection, user_id=user_id)


@app.get("/collections/", response_model=list[schemas.Collection], tags=["collection"])
def read_collections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    collections = crud.get_collections(db, skip=skip, limit=limit)
    return collections


@app.get("/collections/{collection_id}", response_model=schemas.Collection, tags=["collection"])
def read_collection(collection_id: int, db: Session = Depends(get_db)):
    db_collection = crud.get_collection(db, collection_id=collection_id)
    if db_collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return db_collection
