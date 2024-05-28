from pydantic import BaseModel, Field,validator, EmailStr
from typing import Optional

class Comment(BaseModel):
    id: Optional[int] = Field(default=None, title="ID of the comment")
    title: str = Field(..., min_length=1, max_length=100, title="Title of the comment")
    content: str = Field(...,min_length=1, max_length=5000, title="Content of the comment")
    user_id: int = Field(...,ge=1, title="ID of the user who made the comment")
    parche_id: int = Field(...,ge=1, title="ID of the parche the comment is related to")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "title": "Example comment",
                "content": "This is a comment.",
                "user_id": 1,
                "parche_id": 1
            }
        }
 