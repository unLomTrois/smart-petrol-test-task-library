from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.hash import get_password_hash

from app.db import models
from app.schemas import users as user_schemas


def get_user(db: Session, user_id: int):
    user = db.query(models.User).get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(models.User).filter(models.User.name == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    return user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email,
                           hashed_password=hashed_password,
                           name=user.name,
                           role_id=user.role_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# add password hashing
def update_user(db: Session, user: user_schemas.UserUpdate):
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
    return {"message": "deleted successfully"}
