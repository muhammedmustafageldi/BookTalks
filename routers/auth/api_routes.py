import os.path
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from passlib.context import CryptContext
from pydantic import ValidationError
from db.database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from db.models import User
from repositories import auth_repository as repository
from requests_validation import RegisterRequest, Token
from fastapi.security import OAuth2PasswordRequestForm
from .auth_service import authenticate_user, create_access_token
from datetime import timedelta
from helpers import generate_unique_filename

router = APIRouter(
    prefix="/auth",
    tags=["Auth API"]
)

SECRET_KEY = "AkdFRltXkDDzeV4b1BtUYMbpI5dfyyAtC3GBecIVbCSqiwnN2d7kcGhuNNWtZEdE"
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS_DIR = os.path.join('uploaded_images', 'users')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Db_Dependency = Annotated[Session, Depends(get_db)]


### End Points ###
@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: Db_Dependency, email: str = Form(...), username: str = Form(...),password: str = Form(...),profile_image: UploadFile = File(None)):
    # Validate incoming Form fields with Pydantic Model
    try:
        register_request = RegisterRequest(
            email=email,
            username=username,
            password=password)
    except ValidationError as e:
        # Return validation messages if there is erroneous data
        raise HTTPException(status_code=422, detail=e.errors())

    created_user_model = User(
        email=register_request.email,
        username=register_request.username,
        hashed_password=bcrypt_context.hash(register_request.password),
        image_path = "users/default_user_img.png"
    )

    # Save if the user has sent an image
    if profile_image and profile_image.filename:
        unique_filename = generate_unique_filename(profile_image.filename)
        full_file_path = os.path.join(USERS_DIR, unique_filename)
        relative_path = os.path.relpath(full_file_path, "uploaded_images")

        try:
            with open(full_file_path, "wb") as buffer:
                buffer.write(await profile_image.read())
            created_user_model.image_path = relative_path

        except OSError as e:
            raise HTTPException(status_code=500, detail=f"File save error: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    # Add user to database ->
    repository.create_user(db, created_user_model)


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Db_Dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed authentication.")
    token = create_access_token(user.username, user.id, user.role, user.image_path, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
