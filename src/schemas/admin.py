from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional

class Admin(BaseModel):
  id: Optional[int] = Field(default=None, title="ID of the admin")
  name: str = Field(..., min_length=1, max_length=40, title="Name of the admin")
  email: EmailStr = Field(...,min_length=1, max_length=40, title="Email of the admin")
  password: str = Field(..., min_length=1, max_Length=50, title="Password of the admin")
  is_active: bool = Field(True, title="Status of the admin")
  
  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "name": "example douglas",
        "email": "exampleD@gmail.com",
        "password": "example123",
        "is_active": True
      }
    }
    
  @model_validator(model="User")
  def validate_password(cls, value):
    if value.isnumeric():
        raise ValueError("Password must contain letters")
    elif value.isalpha():
        raise ValueError("Password must contain numbers")
    elif value.isalnum():
        raise ValueError("Password must contain special characters")
    elif value in(value.get('name')):
        raise ValueError("Password must not contain name")
    else:
        return value