from typing import Annotated
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import ValidationError
from db.database import SessionLocal
from requests_validation import BookRequest
from helpers import generate_unique_filename
from starlette import status
from db.models import Book

router = APIRouter(tags=["Books"], prefix="/books")

BOOKS_DIR = os.path.join('uploaded_images/books')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Db_Dependency = Annotated[Session, Depends(get_db)]

@router.get("", status_code=status.HTTP_200_OK)
async def get_all_books(db: Db_Dependency):
    return db.query(Book).all()

@router.post("/add_new_book/", status_code=status.HTTP_201_CREATED)
async def add_new_book(db: Db_Dependency,image: UploadFile = File(...),title: str = Form(...),description: str = Form(...),author_id: int = Form(gt=0),rating: int = Form(...),published_date: int = Form(...)
):
    # Validate incoming Form fields with Pydantic Model
    try:
        book_request = BookRequest(
            title=title,
            description=description,
            author_id=author_id,
            rating=rating,
            published_date=published_date
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
            image_path=file_path
        )

        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        return {"message": "Kitap başarıyla eklendi", "book": new_book}
    except OSError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"File save error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
