from pydantic import BaseModel, Field
from typing import Optional

class City(BaseModel):
    id: Optional[int] = Field(default=None, title="ID of the city")
    name: str = Field(min_length=1, max_length=100, title="Name of the city")
    country: str = Field(min_length=2, max_length=100, title="Country of the city")
    zip: str = Field(min_length=4, max_length=10, title="Postal code of the city")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "nombre": "Bogotá",
                "pais": "Colombia",
                "codigo_postal": "110111"
            }
        }