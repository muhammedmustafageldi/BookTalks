from typing import Annotated
from starlette import status
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import User
from ..auth.auth_service import validate_current_user


router = APIRouter(
    tags=['User HTML'],
    prefix="/user"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Db_Dependency = Annotated[Session, Depends(get_db)]
