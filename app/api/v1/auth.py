from datetime import timedelta
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings

from ..utils import authenticate_user, get_current_user_from_token
from app.core.security import create_access_token
from app.schemas.tokens import Token
from app.db import get_db, models

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(data={"sub": user.email},
                                       expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def me(current_user: models.User = Depends(get_current_user_from_token)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.name,
        "role": current_user.role
    }
