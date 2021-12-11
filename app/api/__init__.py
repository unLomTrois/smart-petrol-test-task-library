from fastapi import APIRouter

from .v1 import route_roles, route_users, route_login
from .v1.books import route_books

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(route_books.router, prefix="/books", tags=["books"])
