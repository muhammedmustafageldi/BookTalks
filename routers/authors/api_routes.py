from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
import os
from sqlalchemy.orm import Session
from starlette import status
from db.database import SessionLocal
from typing import Annotated
from db.models import Author
from requests_validation import AuthorRequest
from pydantic import ValidationError
from helpers import generate_unique_filename
from repositories import author_repository as repository

router = APIRouter(
    tags=["Authors API"],
    prefix="/api/authors")

AUTHORS_DIR = os.path.join('uploaded_images', 'authors')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Db_Dependency = Annotated[Session, Depends(get_db)]

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_authors(db: Db_Dependency):
    return repository.get_all_author(db)

@router.post("/add_new_author/", status_code=status.HTTP_201_CREATED)
async def add_new_author(db: Db_Dependency, name: str = Form(), author_info: str = Form(...) ,image: UploadFile = File(...)):
    # Validate incoming Form fields with Pydantic Model
    try:
        author_request = AuthorRequest(name=name, author_info=author_info)
    except ValidationError as e:
        # Return validation messages if there is erroneous data
        raise HTTPException(status_code=422, detail=e.errors())

    unique_filename = generate_unique_filename(image.filename)
    file_path = os.path.join(AUTHORS_DIR, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())

        new_author = Author(name=author_request.name, image_path=file_path, author_info=author_request.author_info)

        # Add author to database ->
        repository.add_author(db, new_author)
        return {"message": "Author successfully added", "author": new_author}

    except OSError as e:  # For file write error
        raise HTTPException(status_code=500, detail=f"File save error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
