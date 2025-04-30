import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from pydantic import ValidationError
from db.database import SessionLocal
from requests_validation import BookRequest
from helpers import generate_unique_filename
from starlette import status
from db.models import Book
from repositories import book_repository as repository
from ..auth.auth_service import validate_current_user

router = APIRouter(
    prefix="/api/books",
    tags=["Books API"]
)

BOOKS_DIR = os.path.join('uploaded_images', 'books')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Db_Dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(validate_current_user)]

#### Endpoints (API ONLY) ->

@router.get("/get_all_books", status_code=status.HTTP_200_OK)
async def get_all_books(user: user_dependency ,db: Db_Dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return repository.get_all_books(db)

@router.post("/add_new_book/", status_code=status.HTTP_201_CREATED)
async def add_new_book(user: user_dependency, db: Db_Dependency,image: UploadFile = File(...),title: str = Form(...),description: str = Form(...),author_id: int = Form(gt=0),rating: int = Form(...),published_date: int = Form(...), page_count: int = Form(...), admin_opinion: str = Form(...)
):
    # Validate user is admin
    if user is None or user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='This request can only be made by admins.')
    # Validate incoming Form fields with Pydantic Model
    try:
        book_request = BookRequest(
            title=title,
            description=description,
            author_id=author_id,
            rating=rating,
            published_date=published_date,
            page_count=page_count,
            admin_opinion=admin_opinion
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

    unique_filename = generate_unique_filename(image.filename)
    file_path = os.path.join(BOOKS_DIR, unique_filename)

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())

        new_book = Book(
            title=book_request.title,
            author_id=book_request.author_id,
            description=book_request.description,
            rating=book_request.rating,
            published_date=book_request.published_date,
            image_path=file_path,
            page_count=book_request.page_count,
            admin_opinion = book_request.admin_opinion
        )

        # Add a book to database ->
        repository.add_book(db, new_book)

        return {"message": "Kitap başarıyla eklendi", "book": new_book}
    except OSError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"File save error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/book_details/", status_code=status.HTTP_200_OK)
async def get_book_details(user: user_dependency, db: Db_Dependency, book_id: int = Query(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    book = repository.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book is not found.")
    return book