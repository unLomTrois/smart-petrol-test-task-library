from fastapi import FastAPI
from app.user import router as user_router

from .db import Base, engine

app = FastAPI()

Base.metadata.create_all(engine)


app.include_router(user_router)
# app.include_router(item_main.router)
