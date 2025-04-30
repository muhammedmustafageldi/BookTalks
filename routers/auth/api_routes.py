from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from db.database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from db.models import User
from repositories import auth_repository as repository
from requests_validation import AuthRequest, Token
from fastapi.security import OAuth2PasswordRequestForm
from .auth_service import authenticate_user, create_access_token
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Auth API"]
)

SECRET_KEY = "AkdFRltXkDDzeV4b1BtUYMbpI5dfyyAtC3GBecIVbCSqiwnN2d7kcGhuNNWtZEdE"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Db_Dependency = Annotated[Session, Depends(get_db)]

### End Points ###
@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: Db_Dependency, create_user_request: AuthRequest):
    create_user_model = User(
        email=create_user_request.email,
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password)
    )
    repository.create_user(db, create_user_model)


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Db_Dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed authentication.")
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}