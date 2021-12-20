from fastapi import APIRouter, Depends
from app.api.utils import check_role
from app.db import Session, get_db

from app.db import crud
from app.schemas import books as book_schemas

# APIRouter creates path operations for user module
router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/", dependencies=[Depends(check_role(["librarian"]))])
async def add_book_item(
    book_item: book_schemas.BookItemCreate, db: Session = Depends(get_db)
):
    return crud.add_book_items(
        db=db, book_id=book_item.parent_book_id, book_count=book_item.count
    )


@router.get("/{book_id}/count", dependencies=[Depends(check_role(["librarian"]))])
async def count_book_items(book_id: int, db: Session = Depends(get_db)):
    return crud.count_book_items(db=db, book_id=book_id)
