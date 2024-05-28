from pydantic import BaseModel, Field,validator, EmailStr
from typing import Optional

class Scenery(BaseModel):
  id: Optional[int] = Field(default=None, title="ID of the scenery")
  name: str = Field(..., title="Name of the scenery")
  description: str = Field(..., title="Description of the scenery")
  capacity: int = Field(..., title="Capacity of the scenery")
  city_id: int = Field(...,ge=1, title="ID of the city")
  
  class config:
    from_attribites = True
    json_schema_extra = {
      "example": {
        "name": "Scenery 1",
        "description": "Description of the scenery 1",
        "capacity": 100,
        "city_id": 1
      }
    }