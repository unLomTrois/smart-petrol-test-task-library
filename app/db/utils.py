import datetime

from sqlalchemy.orm.session import Session

from app.db import models


def get_booking_end_time(days: int = 14):
    return datetime.utcnow() + datetime.timedelta(days=days)


def is_booked(db: Session, book_item_id: int) -> bool:
    """Проверяет, что итем уже забронирован"""

    return db.query(models.Booking).filter(
        models.Booking.book_item_id == book_item_id).scalar()


def is_booked_for_user(db: Session, book_item_id: int, user_id: int) -> bool:
    """Проверяет, что итем уже забронирован конкретному пользователю"""
    return db.query(models.Booking).filter(
        models.Booking.book_item_id == book_item_id,
        models.Booking.user_id == user_id).scalar()


def is_issued(db: Session, book_item_id: int) -> bool:
    """Проверяет, что итем выдан"""

    return db.query(
        models.BookItem).filter(models.BookItem.id == book_item_id,
                                models.BookItem.is_given == True).scalar()


def is_issued_for_user(db: Session, book_item_id: int, user_id: int) -> bool:
    """Проверяет, что итем выдан конкретному пользователю"""

    return db.query(models.BookIssue).filter(
        models.BookIssue.book_item_id == book_item_id,
        models.BookIssue.user_id == user_id).scalar()
