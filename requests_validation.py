from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create', default=None)
    title: str = Field(min_length=3)
    author_id: int = Field(gt=0)
    description: str = Field(min_length=1, max_length=500)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0)
    image_path: Optional[str] = None


class AuthorRequest(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create', default=None)
    name: str = Field(min_length=5)


class AuthRequest(BaseModel):
    email: EmailStr = Field(min_length=10)
    username: str = Field(min_length=5)
    password: str = Field(min_length=6)
