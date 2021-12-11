from fastapi import APIRouter, Depends, status
from app.api.utils import check_role
from app.db import Session, get_db

from app.db import crud
from app.schemas import books as book_schamas

from .book_items import router as route_book_items
from .booking import router as route_booking
from .issues import router as route_issues

# APIRouter creates path operations for user module
router = APIRouter(responses={404: {"description": "Not found"}}, )

router.include_router(route_book_items, prefix="/items", tags=["book_items"])
router.include_router(route_booking, prefix="/booking", tags=["booking"])
router.include_router(route_issues, prefix="/issues", tags=["issues"])


@router.get("/")
async def read_root(db: Session = Depends(get_db)):

    books = crud.get_books(db)

    # print("\n~~~~~~~~~~~~~~:\n", crud.count_book_items(db=db, book_id=1))

    return [
        book.as_dict() | {
            "count": crud.count_book_items(db=db, book_id=book.id)
        } for book in books
    ]


@router.post("/add", dependencies=[Depends(check_role(["librarian"]))])
async def add_book(book: book_schamas.BookCreate,
                   db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@router.delete("/{book_id}/delete",
               status_code=status.HTTP_200_OK,
               dependencies=[Depends(check_role(["librarian"]))])
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    crud.delete_book(db, book_id)
    return {"message": "deleted successfully"}
