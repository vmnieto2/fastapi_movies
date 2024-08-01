from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length = 4, max_length=15)
    overview: str = Field(min_length = 15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length = 3, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "My movie title",
                "overview": "My movie overview",
                "year": 2022,
                "rating": 10,
                "category": "My movie category",
            }
        }
