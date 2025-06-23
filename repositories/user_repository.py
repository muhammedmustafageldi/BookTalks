from sqlalchemy.orm import Session
from db.models import User, favorite_books_table


### QUERIES ->
def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(user_id == User.id).first()

def is_book_in_favorites(db, user_id: int, book_id: int) -> bool:
    result = db.query(favorite_books_table).filter_by(user_id=user_id, book_id=book_id).first()
    return result is not None

### INSERT TRANSACTIONS ->
def add_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)


def add_book_to_favorite(db: Session, user_id: int, book_id: int):
    db.execute(favorite_books_table.insert().values(user_id=user_id, book_id=book_id))
    db.commit()


### DELETE TRANSACTIONS ->
def remove_book_from_favorite(db: Session, user_id: int, book_id: int):
    db.execute(
        favorite_books_table.delete().where(
            (favorite_books_table.c.user_id == user_id) &
            (favorite_books_table.c.book_id == book_id)
        )
    )
    db.commit()


### UPDATE TRANSACTIONS ->