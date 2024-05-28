from pydantic import BaseModel, Field
from typing import Optional

class Category(BaseModel):
  id: Optional[int] = Field(default=None, title="ID of the category")
  name: str = Field(..., min_length=1, max_length=40, title="Name of the category")
  description: str = Field(..., min_length=1, max_length=100, title="Description of the category")
  
  class config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "name": "example category",
        "description": "example description"
      }
    }