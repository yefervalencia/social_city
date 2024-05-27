from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.config.database import Base

class Scenery(Base):
  __tablename__ = "sceneries"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(255), nullable=False)
  description = Column(String(255), nullable=False)
  capacity = Column(Integer, nullable=False)
  
  city = relationship("City", back_populates="sceneries")