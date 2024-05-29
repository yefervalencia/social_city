from typing import List
from src.models.qualification import Qualification as QualificationModel
from src.schemas.qualification import Qualification as QualificationSchema

class QualificationRepository():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_all_qualifications(self,
        offset: int, 
        limit: int
        ) -> List[QualificationSchema]:
        
        query = self.db.query(QualificationModel)
        if(offset is not None):
            query = query.offset(offset)
        if(limit is not None):
            query = query.limit(limit)
        return query.all()

    def get_qualification(self, id: int) -> QualificationSchema:
        element = self.db.query(QualificationModel).filter(QualificationModel.id == id).first()
        return element

    def create_qualification(self, qualification: QualificationSchema) -> dict:
        new_qualification = QualificationModel(**qualification.model_dump())
        self.db.add(new_qualification)
        self.db.commit()
        self.db.refresh(new_qualification)
        return new_qualification
    
    def update_qualification(self, id: int, qualification: QualificationSchema) -> dict:
        element = self.db.query(QualificationModel).filter(QualificationModel.id == id).first()
        element.score = qualification.score
        element.user_id = qualification.user_id
        element.parche_id = qualification.parche_id
        self.db.commit()
        self.db.refresh(element)
        return element
    
    
    def delete_qualification(self, id: int) -> dict:
        element = self.db.query(QualificationModel).filter(QualificationModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element