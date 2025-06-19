from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import Annotated
from sqlalchemy.orm import Session
from requests_validation import CommentRequest
from ..auth.auth_service import validate_current_user
from db.database import SessionLocal
from db.models import Comments
from starlette import status
from repositories import comment_repository as repository
from requests_validation import CommentResponse

router = APIRouter(
    prefix="/api/comments",
    tags=["Comments API"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Db_Dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(validate_current_user)]


#### Endpoints (API ONLY) ->

@router.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def get_comments_by_book_id(user: user_dependency, db: Db_Dependency, book_id: int = Path(..., gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    comments = repository.get_comments_by_book_id(db, book_id)
    return comments


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=CommentResponse)
async def add_comment(user: user_dependency, db: Db_Dependency, comment_request: CommentRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # Create an object
    new_comment = Comments(
        user_id=user['user_id'],
        book_id=comment_request.book_id,
        parent_id=comment_request.parent_id,
        content=comment_request.content
    )
    try:
        repository.add_comment(db, new_comment)
        return new_comment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bir hata oluştu: {str(e)}")

@router.delete("/delete/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(user: user_dependency, db: Db_Dependency, comment_id: int = Query(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    comment = repository.get_single_comment_by_id(db, comment_id)

    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comment is not found.')

    if comment.user.id != user.get('user_id'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this comment.")

    repository.delete_comment(db, comment)
