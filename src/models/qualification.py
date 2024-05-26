from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class Qualification(Base):
    __tablename__ = "qualifications"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    city_id = Column(Integer, ForeignKey('cities.id'))

    user = relationship("User", back_populates="qualifications")
    city = relationship("City", back_populates="qualifications")
