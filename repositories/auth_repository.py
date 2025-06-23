from db.models import User
from sqlalchemy.orm import Session
from sqlalchemy import func


### QUERIES ->
def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(user_id == User.id).first()

def get_user_by_name(db: Session, username: str):
    return db.query(User).filter(username.lower() == func.lower(User.username)).first()

### INSERT TRANSACTIONS ->
def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)


### DELETE TRANSACTIONS ->

### UPDATE TRANSACTIONS ->