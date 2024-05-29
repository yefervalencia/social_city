from typing import List
from src.models.parche import Parche as ParcheModel
from src.schemas.parche import Parche as ParheSchema
import datetime

class ParcheRepository():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_all_parches(self,
        offset: int, 
        limit: int
        ) -> List[ParheSchema]:
        
        query = self.db.query(ParcheModel)
        if(offset is not None):
            query = query.offset(offset)
        if(limit is not None):
            query = query.limit(limit)
        return query.all()

    def get_parche(self, id: int) -> ParheSchema:
        element = self.db.query(ParcheModel).filter(ParcheModel.id == id).first()
        return element

    def create_parche(self, parche: ParheSchema) -> dict:
        new_parche = ParcheModel(**parche.model_dump())
        self.db.add(new_parche)
        self.db.commit()
        self.db.refresh(new_parche)
        return new_parche
    
    def update_parche(self, id: int, parche: ParheSchema) -> dict:
        element = self.db.query(ParcheModel).filter(ParcheModel.id == id).first()
        element.title = parche.title
        element.description = parche.description
        element.start_time = parche.start_time
        element.end_time = parche.end_time
        element.status = parche.status
        element.updated_at = datetime.datetime.now
        element.user_id = parche.user_id
        element.scenery_id = parche.scenery_id
        element.category_id = parche.category_id
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def delete_parche(self, id: int) -> dict:
        element = self.db.query(ParcheModel).filter(ParcheModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element