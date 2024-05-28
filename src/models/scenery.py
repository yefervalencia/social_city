from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base

class Scenery(Base):
  __tablename__ = "sceneries"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(length=50), nullable=False)
  description = Column(String(length=5000), nullable=False)
  capacity = Column(Integer, nullable=False)
  city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
  
  parches = relationship("Parche", back_populates="scenery", cascade="all, delete")
  city = relationship("City", back_populates="sceneries")