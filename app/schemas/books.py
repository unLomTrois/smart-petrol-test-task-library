from datetime import date, datetime
from pydantic import BaseModel

from app.schemas.users import User


class Book(BaseModel):
    id: int
    title: str
    author: str
    language: str
    pages: int
    publication_date: date

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    language: str
    pages: int
    publication_date: date


class BookItem(BaseModel):
    id: int
    parent_book_id: int
    is_booked: bool


class BookItemCreate(BaseModel):
    parent_book_id: int
    count: int
