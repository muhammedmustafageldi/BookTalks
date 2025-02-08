from typing import Optional
from pydantic import BaseModel, Field

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create', default=None)
    title: str = Field(min_length=3)
    author_id: int = Field(gt=0)
    description: str = Field(min_length=1, max_length=500)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0)
    image_path: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Python Programming Basics",
                "author_id": 1,
                "description": "A comprehensive guide to learning Python programming.",
                "rating": 5,
                "published_date": 2023
            }
        }
    }

class AuthorRequest(BaseModel):
    id: Optional[int] = Field(description='Id is not needed on create', default=None)
    name: str = Field(min_length=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Halit Ziya Uşaklıgil"
            }
        }
    }