from sqlalchemy.orm import Session, contains_eager

from fastapi import HTTPException, status

from app.core.hash import get_password_hash

from app.db import models
from app.db.crud.books import get_book_item, get_free_book_item_by_parent
from app.db.crud.users import get_user
from app.db.utils import is_booked, is_issued
from app.schemas import booking as schemas_booking


def get_booking_by_booked_item(db: Session, book_item_id: int):
    return (
        db.query(models.Booking)
        .filter(models.Booking.book_item_id == book_item_id)
        .first()
    )


def get_all_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


def get_all_bookings_of_user(db: Session, user_id: int):
    return db.query(models.Booking).filter(models.Booking.user_id == user_id)


def is_book_already_booked_by_user(db: Session, book_id: int, user_id: int) -> bool:

    return (
        db.query(models.Booking)
        .join(models.Booking.book_item)
        .filter(models.Booking.user_id == user_id)
        .options(contains_eager(models.Booking.book_item))
        .filter(models.BookItem.parent_book_id == book_id)
    ).scalar()


def book_a_book(db: Session, booking: schemas_booking.BookingCreate):
    """Забронировать книгу"""

    user = get_user(db=db, user_id=booking.user_id)
    book_item = get_free_book_item_by_parent(db=db, book_id=booking.book_id)

    if is_book_already_booked_by_user(db, booking.book_id, booking.user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете забронировать одну книгу дважды",
        )

    if is_booked(db=db, book_item_id=book_item.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете забронировать уже забронированную книгу",
        )

    if is_issued(db=db, book_item_id=book_item.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете забронировать уже выданную книгу",
        )

    new_booking = models.Booking(
        user=user, book_item=book_item, end_of_booking=booking.end_of_booking
    )
    # update book item
    book_item.is_booked = True
    db.add(new_booking)
    db.add(book_item)

    db.commit()
    db.refresh(new_booking)

    return {"message": "booked successfully"}


# надо бы сделать кроны для проверки на просрочку бронирования
def unbook_a_book(db: Session, book_item_id: int):
    book_item = get_book_item(db, book_item_id=book_item_id)
    book_item.is_booked = False

    booking = get_booking_by_booked_item(db=db, book_item_id=book_item_id)
    db.delete(booking)
    db.add(book_item)
    db.commit()
    return {"message": "unbooked successfully"}


def unbook_a_book_by_user(db: Session, user_id: int):
    get_all_bookings_of_user(db=db, user_id=user_id).delete()
    db.commit()
    return {"message": "unbooked successfully"}
