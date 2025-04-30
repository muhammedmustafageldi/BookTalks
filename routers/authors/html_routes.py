from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from db.database import SessionLocal
from starlette import status
from repositories import author_repository as repository
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
from ..auth.auth_service import validate_current_user

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


