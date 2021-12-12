from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.api import api_router


def include_router(app: FastAPI):
    app.include_router(api_router)


# def configure_static(app):
#     app.mount("/static", StaticFiles(directory="static"), name="static")


def enable_cors(app: FastAPI):
    origins = [
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI()
    include_router(app)
    enable_cors(app)
    # configure_static(app)
    create_tables()
    return app


app = start_application()
