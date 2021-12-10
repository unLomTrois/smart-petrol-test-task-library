from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Date, String

from app.db import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer,
                primary_key=True,
                nullable=False,
                unique=True,
                autoincrement=True)
    code = Column(String)
    name = Column(String)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,
                primary_key=True,
                nullable=False,
                unique=True,
                autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    role_id = Column(Integer, ForeignKey("roles.id"))
    role: Role = relationship("Role", backref="users")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class BookItem(Base):
    """Конкретный экземпляр книги, которую можно выдавать клиенту"""

    __tablename__ = "book_items"

    id = Column(Integer,
                primary_key=True,
                nullable=False,
                unique=True,
                autoincrement=True)

    # ссылка на абстрактуню книгу, к которой принадлежит данная конкретная
    parent_book_id = Column(Integer, ForeignKey('books.id'))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Book(Base):
    """Абстрактная книга"""

    __tablename__ = "books"

    id = Column(Integer,
                primary_key=True,
                nullable=False,
                unique=True,
                autoincrement=True)
    title = Column(String)
    author = Column(String)
    language = Column(String)
    pages = Column(Integer)
    publication_date = Column(Date)

    items: list[BookItem] = relationship("BookItem")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
