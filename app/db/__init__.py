from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.db.models import Base


# init engine for connection
engine = create_engine(
    "postgresql://testuser:testpass@localhost:5432/testdb",
    echo=True,
)

# init database
Base.metadata.create_all(engine)


# init session
Session = scoped_session(sessionmaker(bind=engine))
