from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from fastapi import Query
from app.db import Session

from app.db.models import Role, User

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_root():
    users = Session.query(User).all()  # .filter_by(name='test').first()

    return [{"name": user.name, "role": user.role} for user in users]


# @router.get("/{user_id}")
# async def read_user(user_id: int):
#     return {"user_id": user_id, "full_name": "Danny Manny", "email": "danny.manny@gmail.com"}

# @router.get("/detail")
# async def read_users(q: Optional[str] = Query(None, max_length=50)):
#     results = {"users": [{"user_id": 1}, {"user_id": 2}]}
#     if q:
#         results.update({"q": q})
#     return results

# @router.post("/add")
# async def add_user(user: User):
#     return {"full_name": user.first_name+" "+user.last_name}

# @router.put("/update")
# async def read_user(user: User):
#     return {"user_id": user.user_id, "full_name": user.first_name+" "+user.last_name, "email": user.email}

# @router.delete("/{user_id}/delete")
# async def read_user(user_id: int):
#     return {"user_id": user_id, "is_deleted": True}
