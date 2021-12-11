from fastapi import APIRouter

from .v1 import roles, users, login
from .v1.books import books

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(books.router, prefix="/books", tags=["books"])
