from typing import Annotated
from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from repositories import user_repository as repository
from requests_validation import PasswordUpdateRequest
from ..auth.auth_service import validate_current_user, verify_password, hash_password
from passlib.context import CryptContext


router = APIRouter(prefix='/api/user', tags=['User API'])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Db_Dependency = Annotated[Session, Depends(get_db)]
UserDependency = Annotated[dict, Depends(validate_current_user)]

@router.get("/current_user")
async def get_current_user(user: UserDependency, db: Db_Dependency):
    if user is None:
        HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is invalid.")

    current_user = repository.get_user_by_id(db, user.get('user_id'))

    if current_user is None:
        HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found.")
    return current_user

@router.put("/update_password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(password_update_request: PasswordUpdateRequest, user: UserDependency, db: Db_Dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    current_user = repository.get_user_by_id(db, user.get('user_id'))
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not found.")

    # is the user password correct
    old_password = password_update_request.old_password
    if verify_password(old_password, current_user.hashed_password) is not True:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect old password")

    # do the new passwords match?
    new_password = password_update_request.new_password
    confirm_password = password_update_request.confirm_new_password

    if new_password != confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")

    current_user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(current_user)

    return {"message": "Password updated successfully"}







