from sqlalchemy.orm import Session
from db.models import Author


### QUERIES ->
def get_all_author(db: Session):
    return db.query(Author).all()

def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(author_id == Author.id).first()

### INSERT TRANSACTIONS ->
def add_author(db: Session, author: Author):
    db.add(author)
    db.commit()
    db.refresh(author)


### DELETE TRANSACTIONS ->

### UPDATE TRANSACTIONS ->
