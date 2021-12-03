from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.db.models import Base
# import os

# init engine for connection
engine = create_engine(
    "postgresql://testuser:testpass@localhost:5432/testdb",
    echo=True,
)

Base.metadata.create_all(engine)

# init database

# init session
Session = scoped_session(sessionmaker(bind=engine))
