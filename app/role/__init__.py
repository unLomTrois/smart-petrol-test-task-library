from fastapi import APIRouter, Depends
from app.db import Session, get_db

from app.db import models, schemas
from app.db.crud.roles import create_role

# APIRouter creates path operations for user module
router = APIRouter(
    prefix="/roles",
    tags=["roles"],
    responses={404: {
        "description": "Not found"
    }},
)


@router.get("/")
async def read_root(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()

    return roles


@router.post("/add")
async def add_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role)


# @router.put("/update")
# async def update_user(user: ):
#     return {"user_id": user.user_id, "full_name": user.first_name+" "+user.last_name, "email": user.email}

# @router.delete("/{user_id}/delete")
# async def read_user(user_id: int):
#     return {"user_id": user_id, "is_deleted": True}
