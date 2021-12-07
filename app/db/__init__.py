from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# init engine for connection
SQLALCHEMY_DATABASE_URL = "postgresql://testuser:testpass@localhost:5432/testdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():  # new
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
