from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional
from datetime import datetime, timedelta
class User (BaseModel):
    id: Optional[int] = Field(default=None, title="Id of the user")
    name: str = Field(min_length=4, max_length=60, title="Name of the user")
    lastname: str = Field(...,title="Lastname of the user")
    email: EmailStr = Field(min_length=6, max_length=64, title="Email of the user")
    password: str = Field(max_length=64, title="Password of the user")
    rol: str = Field(default="user",title="Role of the user")
    is_active: bool = Field(default=True, title="Status of the user")
    born_date: datetime = Field(..., title="Born date of the user")
    cellphone: str = Field(...,min_lenght=10, max_lenght=10, title="Cellphone of the user")
    city_id: int = Field(...,ge=1,title="city of the user")
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "name": "Pepe ",
                "lastname": "Pimentón",
                "email": "pepe@example.com",
                "password": "xxx",
                "rol":"user",
                "is_active": True,
                "born_date" : "2023-1-6T12:00:00",
                "cellphone" : "0000000000",
                "city_id": 1
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
        
    @model_validator(model="User")
    def validate_dates(cls, value):  
        if value.get('born_date') <= (datetime.now() - timedelta(days=14*365.25)):
            raise ValueError("User must be at least 14 years old")
        return value
    
    @model_validator(model="user")
    def validate_rol(cls, value):
        if value.get('rol') not in ["user","admin"]:
            raise ValueError("Invalid role")
        return value
    
class UserLogin (BaseModel):
    email: EmailStr = Field(min_length=6, max_length=64, alias="username", title="Email of the user")
    password: str = Field(min_length=4, title="Password of the user")
