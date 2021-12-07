from sqlalchemy.orm import Session

from app.core.hash import get_password_hash

from app.db import models
from app.schemas import roles as roles_schemas


def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()


def create_role(db: Session, role: roles_schemas.RoleCreate):
    new_role = models.Role(code=role.code, name=role.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role
