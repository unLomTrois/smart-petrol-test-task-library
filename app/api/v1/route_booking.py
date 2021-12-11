from fastapi import APIRouter, Depends
from app.api.utils import check_role
from app.db import Session, get_db

from app.db import crud
from app.schemas import booking as booking_schemas

# APIRouter creates path operations for user module
router = APIRouter(responses={404: {"description": "Not found"}}, )


@router.get("/all", dependencies=[Depends(check_role(["librarian"]))])
async def get_all_bookings(db: Session = Depends(get_db)):
    return crud.get_all_bookings(db=db)


@router.post("/book", dependencies=[Depends(check_role(["librarian"]))])
async def book_a_book(booking: booking_schemas.BookingCreate,
                      db: Session = Depends(get_db)):
    return crud.book_a_book(db=db, booking=booking)


@router.post("/unbook", dependencies=[Depends(check_role(["librarian"]))])
async def unbook(book_item_id: int, db: Session = Depends(get_db)):
    return crud.unbook_a_book(db=db, book_item_id=book_item_id)


# @router.get("/{book_id}/count",
#             dependencies=[Depends(check_role(["librarian"]))])
# async def count_book_items(book_id: int, db: Session = Depends(get_db)):
#     return crud.count_book_items(db=db, book_id=book_id)
