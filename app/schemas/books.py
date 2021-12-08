from datetime import date
from pydantic import BaseModel


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
    language: str
    pages: int
    publication_date: date
