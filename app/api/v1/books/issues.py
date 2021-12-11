from fastapi import APIRouter, Depends
from app.api.utils import check_role
from app.db import Session, get_db

from app.db import crud
from app.schemas.issues import IssueBookForm

# APIRouter creates path operations for user module
router = APIRouter(responses={404: {"description": "Not found"}}, )


@router.get("/", dependencies=[Depends(check_role(["librarian"]))])
async def get_all_issued_books(db: Session = Depends(get_db)):
    return crud.get_all_issued_books(db=db)


@router.get("/all", dependencies=[Depends(check_role(["librarian"]))])
async def get_all_issues(db: Session = Depends(get_db)):
    return crud.get_all_issues(db=db)


@router.post("/", dependencies=[Depends(check_role(["librarian"]))])
async def issue_a_book(issue_form: IssueBookForm,
                       db: Session = Depends(get_db)):
    return crud.issue_a_book(db=db, form=issue_form)


@router.delete("/", dependencies=[Depends(check_role(["librarian"]))])
async def give_a_book_back(book_item_id: int, db: Session = Depends(get_db)):
    return crud.give_book_back(db=db, book_item_id=book_item_id)


# @router.get("/{book_id}/count",
#             dependencies=[Depends(check_role(["librarian"]))])
# async def count_book_items(book_id: int, db: Session = Depends(get_db)):
#     return crud.count_book_items(db=db, book_id=book_id)
