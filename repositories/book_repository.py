from db.models import Book
from sqlalchemy.orm import Session

### QUERIES ->
def get_all_books(db: Session):
    return db.query(Book).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(book_id == Book.id).first()

def get_books_by_author_id(db: Session, author_id: int):
    return db.query(Book).filter(author_id == Book.author_id).all()

def search_books_by_author_and_title(db: Session, author_id: int, query: str):
    return db.query(Book).filter(
        author_id == Book.author_id,
        Book.title.ilike(f"%{query}%")
    ).all()

def search_books_by_name(db: Session, query: str):
    return db.query(Book).filter(Book.title.ilike(f"%{query}%")).all()

### INSERT TRANSACTIONS ->
def add_book(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)


### DELETE TRANSACTIONS ->

### UPDATE TRANSACTIONS ->

