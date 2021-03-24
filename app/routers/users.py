from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..dependencies import get_current_active_user, UserBase, get_db
from ..sql_app import crud, models, schemas
from ..sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)



router = APIRouter(
    prefix='/users',
)


@router.post('/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return crud.create_user(db=db, user=user)


@router.get("/me", response_model=UserBase)
async def read_users_me(current_user: UserBase = Depends(get_current_active_user)):
    return current_user


@router.get("/me/items/")
async def read_own_items(current_user: UserBase = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

