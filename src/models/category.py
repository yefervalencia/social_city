from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from src.config.database import Base

class Category(Base):
  __tablename__ = "categories"
  id = Column(Integer, primary_key=True,autoincrement=True)
  name = Column(String(length=40), unique=True, index=True, nullable=False)
  description = Column(String(length=100), nullable=False)
  
  parches = relationship("Parche", back_populates="category")