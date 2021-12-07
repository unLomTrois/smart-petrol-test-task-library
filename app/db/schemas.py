from typing import Optional
from pydantic import BaseModel


class Role(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True


class RoleCreate(BaseModel):
    code: str
    name: str


class UserBase(BaseModel):
    email: str
    name: str
    role_id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    role_id: Optional[int]

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
