from fastapi import APIRouter, Depends, Request, Query, HTTPException
from db.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette import status
from repositories import comment_repository as repository

router = APIRouter(
    prefix="/comments",
    tags=["Comments HTML"]
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


@router.get("/render_single_comment/", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def render_single_comment(request: Request, db: Db_Dependency, comment_id: int = Query(gt=0)):
    try:
        comment = repository.get_single_comment_by_id(db, comment_id)
        if comment is None:
            raise HTTPException(status_code=404, detail="Comment is not found.")
        return templates.TemplateResponse('/partials/comment_partial.html', {'request': request, 'comment': comment})
    except Exception as e:
        print(f"Error: {e}")
        # An error occurred return state
        raise HTTPException(status_code=500, detail="A server error occurred")
