from fastapi import APIRouter, Depends, status
from app.db import Session, crud, get_db

from app.db import crud
from app import schemas


# APIRouter creates path operations for user module
router = APIRouter(responses={404: {"description": "Not found"}}, )


@router.get("/")
async def read_root(db: Session = Depends(get_db)):
    users = crud.get_users(db)

    return [{
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    } for user in users]



# @router.get("/users/me/", response_model=schemas.User)
# async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
#     return current_user


# @router.get("/{user_id}")
# async def read_user(user_id: int):
#     return {"user_id": user_id, "full_name": "Danny Manny", "email": "danny.manny@gmail.com"}


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role_id": new_user.role_id
    }


@router.put("/update", status_code=status.HTTP_200_OK)
async def update_user(user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user)

    return {
        "id": updated_user.id,
        "name": updated_user.name,
        "email": updated_user.email,
        "role_id": updated_user.role_id
    }


@router.delete("/{user_id}/delete", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return {"message": "deleted successfully"}
