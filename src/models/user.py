from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.config.database import Base
import datetime

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(length=60), index=True)
  lastname = Column(String(length=60), nullable=False)
  email = Column(String(length=64), unique=True,nullable=False)
  password = Column(String, nullable=False)
  born_date = Column(DateTime, nullable=False)
  created_at = Column(DateTime, default=datetime.datetime.now)
  updated_at = Column()
  cellphone = Column(String (length=10), nullable=False)
  is_active = Column(Boolean, default=True)
  city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
  
  city = relationship("City", back_populates="users")