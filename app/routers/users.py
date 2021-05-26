from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_current_active_user, get_db
from ..sql_app import crud, models, schemas
from ..sql_app.database import engine
from ..sql_app.schemas import User, UserBase

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
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    current_user = UserBase(username=current_user.username, full_name=current_user.full_name,
                            email=current_user.email)
    return current_user

