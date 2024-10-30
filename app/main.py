from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine
from app.routers import users #, cards, collections, train_records


models.metadata.create_all(bind=engine)

app = FastAPI()


#app.include_router(cards.router)
#app.include_router(collections.router)
#app.include_router(train_records.router)
app.include_router(users.router)


"""@app.get("/profile", response_model=schemas.user.User, tags=["profile"])
def read_current_user_profile(db: Session = Depends(get_db)):
    db_profile = crud.user.get_profile(db)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_profile"""
