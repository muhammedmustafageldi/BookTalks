from datetime import datetime, UTC
from sqlalchemy.orm import relationship
from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table

favorite_books_table = Table(
    'favorite_books',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True, index=True),
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True, index=True),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    image_path = Column(String, default="users/default_user_img.png")

    comments = relationship('Comments', back_populates='user')
    favorite_books = relationship('Book', secondary=favorite_books_table, back_populates='favorite_by')


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False, index=True)
    description = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    published_date = Column(Integer, nullable=False)
    image_path = Column(String, default=None)
    page_count = Column(Integer, nullable=False)
    admin_opinion = Column(String, nullable=False)

    author = relationship('Author', back_populates='books')
    comments = relationship('Comments', back_populates='book', cascade='all, delete')
    favorite_by = relationship('User', secondary=favorite_books_table, back_populates='favorite_books')

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    author_info = Column(String, nullable=False)
    image_path = Column(String, default=None)

    books = relationship('Book', back_populates='author')


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('comments.id'), nullable=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    user = relationship('User', back_populates='comments')
    book = relationship('Book', back_populates='comments')
    parent = relationship('Comments', remote_side=[id], back_populates='replies')
    replies = relationship('Comments', back_populates='parent', cascade="all, delete-orphan")