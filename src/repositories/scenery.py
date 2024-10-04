from typing import List
from src.schemas.scenery import Scenery as ScenerySchema
from src.models.scenery import Scenery as SceneryModel

class SceneryRepository():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_all_sceneries(self,
        offset: int, 
        limit: int
        ) -> List[SceneryModel]:
        
        query = self.db.query(SceneryModel)
        if(offset is not None):
            query = query.offset(offset)
        if(limit is not None):
            query = query.limit(limit)
        return query.all()
    
    def get_sceneries_city(self,
        offset: int, 
        limit: int,
        idCity
        ) -> List[SceneryModel]:
        
        query = self.db.query(SceneryModel).filter(SceneryModel.city_id == idCity)
        if(offset is not None):
            query = query.offset(offset)
        if(limit is not None):
            query = query.limit(limit)
        return query.all()

    def get_scenery(self, id: int) -> ScenerySchema:
        element = self.db.query(SceneryModel).filter(SceneryModel.id == id).first()
        return element

    def create_scenery(self, scenery: ScenerySchema) -> dict:
        new_scenery = SceneryModel(**scenery.model_dump())
        self.db.add(new_scenery)
        self.db.commit()
        self.db.refresh(new_scenery)
        return new_scenery
    
    def update_scenery(self, id: int, scenery: ScenerySchema) -> dict:
        element = self.db.query(SceneryModel).filter(SceneryModel.id == id).first()
        element.name = scenery.name
        element.description  = scenery.description
        element.capacity = scenery.capacity
        element.city_id = scenery.city_id
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def delete_scenery(self, id: int) -> dict:
        element = self.db.query(SceneryModel).filter(SceneryModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element