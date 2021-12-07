from fastapi import FastAPI
from app.db import Base, engine
from app.api import api_router

def include_router(app: FastAPI):
    app.include_router(api_router)


# def configure_static(app):
#     app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI()
    include_router(app)
    # configure_static(app)
    create_tables()
    return app


app = start_application()
