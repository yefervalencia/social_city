from pydantic import BaseModel, Field,validator, EmailStr
from typing import Optional

class City(BaseModel):
    id: Optional[int] = Field(default=None, title="ID of the city")
    name: str = Field(...,min_length=1, max_length=100, title="Name of the city")
    country: str = Field(...,min_length=2, max_length=100, title="Country of the city")
    zip: int = Field(...,min_length=5, max_length=5, title="Postal code of the city")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "nombre": "Bogotá",
                "pais": "Colombia",
                "codigo_postal": 11011
            }
        } 