from sqlalchemy.orm import Session
from db.models import User

### QUERIES ->
def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(user_id == User.id).first()

### INSERT TRANSACTIONS ->
def add_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)


### DELETE TRANSACTIONS ->

### UPDATE TRANSACTIONS ->