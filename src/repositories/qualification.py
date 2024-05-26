from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from sqlalchemy.orm import Session
from src.models.qualification import Qualification as QualificationModel
from src.schemas.qualification import Qualification as QualificationSchema

class QualificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_qualifications(self, offset: int = 0, limit: int = 10):
        return self.db.query(QualificationModel).offset(offset).limit(limit).all()

    def get_qualification(self, qualification_id: int):
        return self.db.query(QualificationModel).filter(QualificationModel.id == qualification_id).first()

    def create_qualification(self, qualification: QualificationSchema):
        db_qualification = QualificationModel(
            score=qualification.score,
            user_id=qualification.user_id,
            city_id=qualification.city_id
        )
        self.db.add(db_qualification)
        self.db.commit()
        self.db.refresh(db_qualification)
        return db_qualification

    def update_qualification(self, qualification_id: int, qualification: QualificationSchema):
        db_qualification = self.get_qualification(qualification_id)
        if db_qualification:
            db_qualification.score = qualification.score
            db_qualification.user_id = qualification.user_id
            db_qualification.city_id = qualification.city_id
            self.db.commit()
            self.db.refresh(db_qualification)
        return db_qualification

    def delete_qualification(self, qualification_id: int):
        db_qualification = self.get_qualification(qualification_id)
        if db_qualification:
            self.db.delete(db_qualification)
            self.db.commit()
        return db_qualification
