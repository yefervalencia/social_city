from pydantic import BaseModel, Field
from typing import Optional

class Qualification(BaseModel):
    id: Optional[int] = Field(default=None, title="ID of the qualification")
    score: float = Field(ge=1, le=5, title="Score of the qualification (1-5)")
    user_id: int = Field(...,ge=1, title="ID of the user who gave the qualification")
    city_id: int = Field(...,ge=1, title="ID of the city being qualified")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "score": 4,
                "user_id": 1,
                "city_id": 1
            }
        } 
