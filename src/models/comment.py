from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    city_id = Column(Integer, ForeignKey('cities.id'))

    user = relationship("User", back_populates="comments")
    city = relationship("City", back_populates="comments")
