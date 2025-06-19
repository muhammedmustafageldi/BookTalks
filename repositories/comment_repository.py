from db.models import Comments
from sqlalchemy.orm import Session


### QUERIES ->
def get_comments_by_book_id(db: Session, book_id: int):
    return db.query(Comments).filter(book_id == Comments.book_id).order_by(Comments.created_at.desc()).all()


def get_single_comment_by_id(db: Session, comment_id: int):
    return db.query(Comments).filter(comment_id == Comments.id).first()


### INSERT TRANSACTIONS ->
def add_comment(db: Session, comment: Comments):
    db.add(comment)
    db.commit()
    db.refresh(comment)


### DELETE TRANSACTIONS ->
def delete_comment(db: Session, comment: Comments):
    db.delete(comment)
    db.commit()