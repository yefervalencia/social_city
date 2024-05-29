from typing import List
from src.models.city import City as CityModel
from src.schemas.city import City as CitySchema

class CityRepository():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_all_cities(self,
        offset: int, 
        limit: int
        ) -> List[CitySchema]:
        
        query = self.db.query(CityModel)
        if(offset is not None):
            query = query.offset(offset)
        if(limit is not None):
            query = query.limit(limit)
        return query.all()

    def get_city(self, id: int) -> CitySchema:
        element = self.db.query(CityModel).filter(CityModel.id == id).first()
        return element

    def create_city(self, city: CitySchema) -> dict:
        new_city = CityModel(**city.model_dump())
        self.db.add(new_city)
        self.db.commit()
        self.db.refresh(new_city)
        return new_city
    
    def update_city(self, id: int, city: CitySchema) -> dict:
        element = self.db.query(CityModel).filter(CityModel.id == id).first()
        element.name = city.name
        element.country = city.country
        element.zip = city.zip
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def delete_city(self, id: int) -> dict:
        element = self.db.query(CityModel).filter(CityModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element