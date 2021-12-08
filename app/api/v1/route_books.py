from fastapi import APIRouter, Depends
from app.api.utils import RoleChecker
from app.db import Session, get_db

from app.db import models
from app.db.crud.books import get_books, create_book
from app.schemas import books as book_schamas

# APIRouter creates path operations for user module
router = APIRouter(responses={404: {"description": "Not found"}}, )

allow_create_resource = RoleChecker(["booker"])


@router.get("/", dependencies=[Depends(allow_create_resource)])
async def read_root(db: Session = Depends(get_db)):

    books = get_books(db)

    return books


@router.post("/add")
async def add_book(book: book_schamas.BookCreate,
                   db: Session = Depends(get_db)):
    return create_book(db, book)
