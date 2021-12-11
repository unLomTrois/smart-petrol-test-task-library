from sqlalchemy.orm import Session

from fastapi import HTTPException, status

from app.core.hash import get_password_hash

from app.db import models
from app.db.crud.books import get_book_item
from app.db.crud.users import get_user
from app.db.utils import is_booked, is_issued
from app.schemas import booking as schemas_booking


def get_booking_by_booked_item(db: Session, book_item_id: int):
    return db.query(models.Booking).filter(
        models.Booking.book_item_id == book_item_id).first()


def get_all_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()


def book_a_book(db: Session, booking: schemas_booking.BookingCreate):
    """Забронировать книгу"""

    user = get_user(db=db, user_id=booking.user_id)
    book_item = get_book_item(db=db, book_item_id=booking.book_item_id)

    if is_booked(db=db, book_item_id=booking.book_item_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете забронировать уже забронированную книгу",
        )

    if is_issued(db=db, book_item_id=booking.book_item_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Вы не можете забронировать уже выданную книгу",
        )

    new_booking = models.Booking(user=user,
                                 book_item=book_item,
                                 end_of_booking=booking.end_of_booking)
    # update book item
    book_item.is_booked = True
    db.add(new_booking)
    db.add(book_item)

    db.commit()
    db.refresh(new_booking)
    return new_booking


# надо бы сделать кроны для проверки на просрочку бронирования
def unbook_a_book(db: Session, book_item_id: int):
    book_item = get_book_item(db, book_item_id=book_item_id)
    book_item.is_booked = False

    booking = get_booking_by_booked_item(db=db, book_item_id=book_item_id)
    db.delete(booking)
    db.add(book_item)
    db.commit()
    return {"message": "unbooked successfully"}
