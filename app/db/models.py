from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String


Base = declarative_base()


class Role(Base):
    __tablename__ = "roles"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    name = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer, primary_key=True, nullable=False, unique=True, autoincrement=True
    )
    name = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", backref="users")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
