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
from repositories import user_repository
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
):    # Validate user is admin
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

    # Example: abc.jpg
    unique_filename = generate_unique_filename(image.filename)

    # Example: uploaded_images/books/abc.jpeg
    full_file_path = os.path.join(BOOKS_DIR, unique_filename)

    # Example: books/abc.jpeg
    relative_path = os.path.relpath(full_file_path, "uploaded_images")

    try:
        with open(full_file_path, "wb") as buffer:
            buffer.write(await image.read())

        new_book = Book(
            title=book_request.title,
            author_id=book_request.author_id,
            description=book_request.description,
            rating=book_request.rating,
            published_date=book_request.published_date,
            image_path=relative_path,
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


@router.post("/add_book_to_favorites/", status_code=status.HTTP_201_CREATED)
async def add_book_to_favorites(user: user_dependency, db: Db_Dependency, book_id: int = Query(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Book check
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")
    # Check is book in favorite
    exists = user_repository.is_book_in_favorites(db, user.get('user_id'), book_id)
    if exists:
        raise HTTPException(status_code=400, detail="Book is already in favorites.")
    try:
        user_repository.add_book_to_favorite(db, user.get('user_id'), book_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")


@router.post("/remove_book_from_favorites/", status_code=status.HTTP_200_OK)
async def remove_book_from_favorites(user: user_dependency, db: Db_Dependency, book_id: int = Query(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Book check
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found.")

    # Check is book in favorite
    exists = user_repository.is_book_in_favorites(db, user.get('user_id'), book_id)
    if not exists:
        raise HTTPException(status_code=400, detail="Book is not in favorites.")

    try:
        user_repository.remove_book_from_favorite(db, user.get('user_id'), book_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred: {e}")
