from fastapi import APIRouter, Depends, Request, Path
from sqlalchemy.orm import Session, Query
from db.database import SessionLocal
from starlette import status
from repositories import author_repository as repository
from repositories import book_repository as book_repository
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
from ..auth.auth_service import validate_current_user, redirect_to_login

router = APIRouter(
    prefix="/authors",
    tags=["Authors HTML"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Db_Dependency = Annotated[Session, Depends(get_db)]

# Define templates directory
templates = Jinja2Templates(directory="templates")

### HTML Responses ->
@router.get("", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def all_authors_render(request: Request, db: Db_Dependency):
    try:
        user = await validate_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        authors = repository.get_all_author(db)
        return templates.TemplateResponse('authors.html', {'request': request, 'authors': authors, 'user': user})

    except:
        return redirect_to_login()


@router.get("/author_details/{author_id}", response_class=HTMLResponse)
async def author_details_render(request: Request, db: Db_Dependency, author_id: int = Path(gt=0)):
    try:
        user = await validate_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        author = repository.get_author_by_id(db, author_id)
        author_books = book_repository.get_books_by_author_id(db, author.id)
        return templates.TemplateResponse('author_details.html', {'request': request, 'author': author, 'author_books': author_books,'user':user})

    except:
        return redirect_to_login()


@router.get("/author_details/{author_id}/search", response_class=HTMLResponse)
async def search_books_by_author(request: Request, db: Db_Dependency, author_id: int = Path(gt=0), query: str = ""):
    try:
        user = await validate_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        # Search books ->
        filtered_books = book_repository.search_books_by_author_and_title(db, author_id, query)

        return templates.TemplateResponse('/partials/author_book_list.html', {
            "request": request,
            "author_books": filtered_books
        })
    except:
        return HTMLResponse("<p>Bir hata oluştu.</p>", status_code=500)