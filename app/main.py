from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import engine, get_db
from app.routers import cards, collections, train_records, users


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(cards.router)
app.include_router(collections.router)
app.include_router(train_records.router)
app.include_router(users.router)


@app.get("/profile", response_model=schemas.user.User, tags=["profile"])
def read_current_user_profile(db: Session = Depends(get_db)):
    db_profile = crud.user.get_profile(db)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_profile
