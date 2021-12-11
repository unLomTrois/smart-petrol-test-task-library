from fastapi import APIRouter, Depends
from app.db import Session, get_db

from app.db import models
from app.db.crud.roles import create_role
from app import schemas


# APIRouter creates path operations for user module
router = APIRouter(responses={404: {"description": "Not found"}}, )


@router.get("/")
async def read_root(db: Session = Depends(get_db)):
    roles = db.query(models.Role).all()

    return roles


@router.post("/add")
async def add_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role)
