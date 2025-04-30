from db.models import Book
from sqlalchemy.orm import Session

### QUERIES ->
def get_all_books(db: Session):
    return db.query(Book).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(book_id == Book.id).first()

### INSERT TRANSACTIONS ->
def add_book(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)


### DELETE TRANSACTIONS ->

### UPDATE TRANSACTIONS ->

