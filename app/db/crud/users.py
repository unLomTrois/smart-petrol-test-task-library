from os import name
from sqlalchemy.orm import Session

from app.core.hash import get_password_hash

from .. import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email,
                           hashed_password=hashed_password,
                           name=user.name,
                           role_id=user.role_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user: schemas.UserUpdate):
    db_user = db.query(
        models.User).filter(models.User.id == user.id).one_or_none()
    if db_user is None:
        return None

    # Update model class variable from requested fields # **typo** was vars(db_user) => vars(user)
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
