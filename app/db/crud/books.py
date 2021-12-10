from sqlalchemy.orm import Session

from app.core.hash import get_password_hash

from app.db import models
from app.schemas import books as schemas_book


def get_book_item(db: Session, book_id: int):
    return db.query(
        models.BookItem).filter(models.BookItem.parent_book_id == book_id)


def count_book_items(db: Session, book_id: int):
    return db.query(models.BookItem).filter(
        models.BookItem.parent_book_id == book_id).count()


def count_free_book_items(db: Session, book_id: int):
    return db.query(models.BookItem).filter(
        models.BookItem.parent_book_id == book_id).count()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas_book.BookCreate):
    new_book = models.Book(title=book.title,
                           author=book.author,
                           language=book.language,
                           pages=book.pages,
                           publication_date=book.publication_date)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def delete_book(db: Session, book_id: int):
    user = get_book(db, book_id)
    db.delete(user)
    db.commit()
