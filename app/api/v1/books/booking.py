from fastapi import APIRouter, Depends
from app.api.utils import check_role
from app.db import Session, get_db

from app.db import crud
from app.schemas import booking as booking_schemas

# APIRouter creates path operations for user module
router = APIRouter(
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(check_role(["client", "admin", "librarian"]))],
)


@router.get("/all")
async def get_all_bookings(db: Session = Depends(get_db)):
    return crud.get_all_bookings(db=db)


@router.get("/{book_id}/{user_id}")
async def is_booked_by_user(book_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.is_book_already_booked_by_user(db, book_id, user_id)


@router.post("/book")
async def book_a_book(
    booking: booking_schemas.BookingCreate, db: Session = Depends(get_db)
):
    return crud.book_a_book(db=db, booking=booking)


@router.delete("/unbook/{book_item_id}")
async def unbook(book_item_id: int, db: Session = Depends(get_db)):
    return crud.unbook_a_book(db=db, book_item_id=book_item_id)


# @router.get("/{book_id}/count",
#             dependencies=[Depends(check_role(["librarian"]))])
# async def count_book_items(book_id: int, db: Session = Depends(get_db)):
#     return crud.count_book_items(db=db, book_id=book_id)
