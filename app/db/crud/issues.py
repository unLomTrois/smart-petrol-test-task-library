from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.core.hash import get_password_hash

from app.db import models
from app.db.crud.books import get_book_item, get_book_item_by_parent, get_free_book_item_by_parent
from app.db.crud.users import get_user
from app.db.utils import is_booked, is_booked_for_user, is_issued
from app.schemas.issues import IssueBookForm


def get_issue_by_book_item(db: Session, book_item_id: int):
    return (
        db.query(models.BookIssue)
        .filter(models.BookIssue.book_item_id == book_item_id)
        .first()
    )


def get_all_issued_books(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.BookItem)
        .filter(models.BookItem.is_given == True)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_issues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BookIssue).offset(skip).limit(limit).all()


def issue_a_book(db: Session, form: IssueBookForm):
    """Выдать книгу"""

    user = get_user(db=db, user_id=form.user_id)
    book_item = get_free_book_item_by_parent(db=db, book_id=form.book_id)

    # if is_booked(db=db, book_item_id=book_item.id) and not is_booked_for_user(
    #     db=db, book_item_id=book_item.id, user_id=form.user_id
    # ):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Вы не можете выдать книгу пользователю, если она уже забронирована не для него",
    #     )

    # if is_issued(db=db, book_item_id=form.book_item_id):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Вы не можете выдать уже выданную книгу",
    #     )

    new_issue = models.BookIssue(
        user=user, book_item=book_item, end_of_issue=form.end_of_issue
    )
    # update book item
    book_item.is_given = True
    db.add(new_issue)
    db.add(new_issue)

    db.commit()
    db.refresh(new_issue)
    return new_issue


# надо бы сделать кроны для проверки на просрочку бронирования
def give_book_back(db: Session, book_item_id: int):
    book_item = get_book_item(db, book_item_id=book_item_id)
    book_item.is_given = False

    issue = get_issue_by_book_item(db=db, book_item_id=book_item_id)
    db.delete(issue)
    db.add(book_item)
    db.commit()
    return {"message": "unbooked successfully"}
