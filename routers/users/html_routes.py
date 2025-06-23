from typing import Annotated
from starlette import status
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from repositories import user_repository as repository
from db.database import SessionLocal
from ..auth.auth_service import validate_current_user, redirect_to_login

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

# Define templates directory
templates = Jinja2Templates(directory="templates")

### HTML Responses ->
@router.get("/profile", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_current_user_profile(request: Request, db: Db_Dependency):
    try:
        user = await validate_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        # Get user data
        current_user = repository.get_user_by_id(db, user.get('user_id'))
        if current_user is None:
            raise HTTPException(status_code=404, detail="Error: user is not found.")

        return templates.TemplateResponse("profile.html", {'request': request, 'user': current_user})

    except Exception as e:
        print(f"Error: ${e}")
        return redirect_to_login()

