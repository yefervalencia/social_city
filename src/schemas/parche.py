from pydantic import BaseModel, Field, model_validator
from typing import Optional 
from datetime import datetime

class Parche(BaseModel):  
  id: Optional[int] = Field(default=None, title="ID of the parche")
  title: str = Field(..., min_length=1, max_length=30, title="Title of the parche")
  description: str = Field(..., min_length=1,max_Lenght=5000, title="Description of the parche")
  start_time: Optional[datetime] = Field(default=datetime.now(), title="Start time of the parche")
  end_time: datetime = Field(..., title="End time of the parche")
  status: bool = Field(default=True, title="Status of the parche")
  user_id: int = Field(...,ge=1, title="ID of the user")
  scenery_id: int = Field(...,ge=1, title="ID of the scenery")
  category_id: int = Field(...,ge=1, title="ID of the category")
  
  class config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "title": "example parche",
        "description": "example description",
        "start_time" : "2022-12-12T12:00:00",
        "end_time": "2023-1-6T12:00:00",
        "user_id": 1,
        "scenery_id": 1,
        "category_id": 1
      }
    }
  
  # @model_validator(mode='after')
  # def validate_dates(self):
  #   start_time = self.start_time
  #   end_time = self.end_time
    
  #   if start_time >= datetime.now():
  #       raise ValueError("Start time must be greater than the current time")
    
  #   if end_time >= start_time:
  #       raise ValueError("End time must be greater than the start time")
    
  #   return self