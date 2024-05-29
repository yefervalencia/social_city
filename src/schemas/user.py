from pydantic import BaseModel, Field, EmailStr, model_validator
from typing import Optional
from datetime import datetime, timedelta
class User (BaseModel):
    id: Optional[int] = Field(default=None, title="Id of the user")
    name: str = Field(min_length=4, max_length=60, title="Name of the user")
    lastname: str = Field(...,title="Lastname of the user")
    email: EmailStr = Field(min_length=6, max_length=64, title="Email of the user")
    password: str = Field(title="Password of the user")
    rol: str = Field(default="user",title="Rol of the user")
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
    
    @model_validator(mode='after')
    def validate_password(self):
        if self.password.isnumeric():
            raise ValueError("Password must contain letters")
        elif self.password.isalpha():
            raise ValueError("Password must contain numbers")
        elif self.password.isalnum():
            raise ValueError("Password must contain special characters")
        elif (self.name.lower()) in self.password or (self.lastname.lower()) in self.password:
            raise ValueError("Password must not contain name")
        else:
            return self
        
    @model_validator(mode='after')
    def validate_dates(self):  
        if self.born_date >= (datetime.now() - timedelta(days=14*365.25)):
            raise ValueError("User must be at least 14 years old")
        return self
    
    @model_validator(mode='after')
    def validate_rol(self):
        if self.rol not in ["user","admin"]:
            raise ValueError("Invalid rol")
        return self
    
class UserLogin (BaseModel):
    email: EmailStr = Field(min_length=6, max_length=64, alias="username", title="Email of the user")
    password: str = Field(min_length=4, title="Password of the user")
