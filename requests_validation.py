from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create', default=None)
    title: str = Field(min_length=3)
    author_id: int = Field(gt=0)
    description: str = Field(min_length=1, max_length=500)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0)
    image_path: Optional[str] = None
    page_count: int = Field(gt=0)
    admin_opinion: str = Field(min_length=1, max_length=300)


class AuthorRequest(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create', default=None)
    name: str = Field(min_length=5)
    author_info: str = Field(min_length=1, max_length=450)


class AuthRequest(BaseModel):
    email: EmailStr = Field(min_length=10)
    username: str = Field(min_length=5)
    password: str = Field(min_length=6)


class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordUpdateRequest(BaseModel):
    old_password: str = Field(..., min_length=6)
    new_password: str = Field(..., min_length=6)
    confirm_new_password: str = Field(..., min_length=6)

class CommentRequest(BaseModel):
    book_id: int = Field(..., gt=0)
    parent_id: Optional[int] = Field(None, description="ID of the parent comment if this is a reply. If not, leave it blank.")
    content: str = Field(..., min_length=1)

class CommentResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    parent_id: int | None
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

