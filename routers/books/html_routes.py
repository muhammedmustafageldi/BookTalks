from typing import Annotated
from fastapi import APIRouter, Depends, Request, Path
from sqlalchemy.orm import Session
from db.database import SessionLocal
from starlette import status
from repositories import book_repository as repository
from ..auth.auth_service import validate_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/books",
    tags=["Books HTML"]
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

# Define redirect
def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response


### HTML Responses ->
@router.get("", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def all_books_render(request: Request, db: Db_Dependency):
    try:
        user = await validate_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        books = repository.get_all_books(db)
        return templates.TemplateResponse("books.html", {'request': request, 'books': books, 'user': user})
    except:
        return redirect_to_login()

@router.get("/book_details/{book_id}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def book_details_render(request: Request, db: Db_Dependency, book_id: int = Path(gt=0)):
    try:
        user = await validate_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        book = repository.get_book_by_id(db, book_id)
        return templates.TemplateResponse("book_details.html", {'request': request, 'book': book, 'user': user})
    except:
        return redirect_to_login()
