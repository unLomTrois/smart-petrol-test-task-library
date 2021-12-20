from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.hash import get_password_hash

from app.db import models
from app.schemas import books as schemas_book


def get_book_item(db: Session, book_item_id: int):
    book = db.query(models.BookItem).get(book_item_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена",
        )

    return book


def get_book_item_by_parent(db: Session, book_id: int):
    return (
        db.query(models.BookItem)
        .filter(models.BookItem.parent_book_id == book_id)
        .first()
    )


def get_free_book_item_by_parent(db: Session, book_id: int):
    return (
        db.query(models.BookItem)
        .filter(
            models.BookItem.parent_book_id == book_id,
            models.BookItem.is_booked == False,
            models.BookItem.is_given == False,
        )
        .order_by(models.BookItem.id)
        .first()
    )


def count_book_items(db: Session, book_id: int):
    return (
        db.query(models.BookItem)
        .filter(models.BookItem.parent_book_id == book_id)
        .count()
    )


def count_free_book_items(db: Session, book_id: int):
    return (
        db.query(models.BookItem)
        .filter(
            models.BookItem.parent_book_id == book_id,
            models.BookItem.is_booked == False,
            models.BookItem.is_given == False,
        )
        .count()
    )


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas_book.BookCreate):
    new_book = models.Book(
        title=book.title,
        author=book.author,
        description=book.description,
        language=book.language,
        pages=book.pages,
        publication_date=book.publication_date,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def delete_book(db: Session, book_id: int):
    user = get_book(db, book_id)
    db.delete(user)
    db.commit()
    return {"message": "deleted successfully"}


def add_book_item(db: Session, book_id: int):
    new_book_item = models.BookItem(parent_book_id=book_id)
    db.add(new_book_item)
    db.commit()
    db.refresh(new_book_item)
    return new_book_item


def add_book_items(db: Session, book_id: int, book_count: int = 1):
    new_book_itmes = [
        models.BookItem(parent_book_id=book_id) for _ in range(book_count)
    ]
    db.add_all(new_book_itmes)
    db.commit()
    
    new_items_count = len(new_book_itmes)
    message = f"{new_items_count} новых экземпляров было добавлено"

    return {"message": message }
