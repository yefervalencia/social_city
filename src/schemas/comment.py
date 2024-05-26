from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from pydantic import BaseModel, Field
from typing import Optional

class Comment(BaseModel):
    id: Optional[int] = Field(default=None, title="ID of the comment")
    content: str = Field(min_length=1, max_length=500, title="Content of the comment")
    user_id: int = Field(..., title="ID of the user who made the comment")
    city_id: int = Field(..., title="ID of the city the comment is related to")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "content": "This is a comment.",
                "user_id": 1,
                "city_id": 1
            }
        }
