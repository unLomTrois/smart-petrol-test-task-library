from typing import Dict
from typing import Optional

from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.params import Depends
from fastapi.security import OAuth2
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.orm.session import Session
from jose import JWTError, jwt

from app.core.hash import verify_password
from app.core.config import settings
from app.db import get_db, models
from app.db.crud.users import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def authenticate_user(username: str,
                      password: str,
                      db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=username)
    print(user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user_from_token(token: str = Depends(oauth2_scheme),
                                db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token,
                             settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        print("username/email extracted is ", email)
        if email is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
        )
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db=db, email=email)
    if user is None:
        raise credentials_exception
    return user


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={
            "tokenUrl": tokenUrl,
            "scopes": scopes
        })
        super().__init__(flows=flows,
                         scheme_name=scheme_name,
                         auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(
            "access_token"
        )  # changed to accept access token from httpOnly Cookie

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


def check_role(allowed_roles: list[str]):
    def _check_role(user: models.User = Depends(get_current_user_from_token)):
        if user.role.code not in allowed_roles:
            # logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=403,
                                detail="Operation not permitted")

    return _check_role
