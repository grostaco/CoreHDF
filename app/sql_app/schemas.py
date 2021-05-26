from pydantic import BaseModel
from typing import List
"""
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

"""


class UserBase(BaseModel):
    username: str
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    hashed_password: str
    is_active: bool = True
    permissions: int = 0

    class Config:
        orm_mode = True


class Log(BaseModel):
    level: str
    datetime: str
    message: str


class LogResponse(BaseModel):
    logs: List[Log]


