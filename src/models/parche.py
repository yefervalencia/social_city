from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from src.config.database import Base
import datetime

class Parche(Base):
  __tablename__ = "parches"
  
  id = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(length=30), index=True, nullable=False)
  description = Column(String(length=5000),nullable=False)
  start_time = Column(DateTime, default=datetime.datetime.now)
  end_time = Column(DateTime, nullable=False)
  status = Column(Boolean, default=True)
  created_at= Column(DateTime, default=datetime.datetime.now)
  updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
  user_id = Column(Integer, ForeignKey('users.id'))
  scenery_id = Column(Integer, ForeignKey('sceneries.id'))
  category_id = Column(Integer, ForeignKey('categories.id'))
  
  user = relationship("User", back_populates="parches")
  scenery = relationship("Scenery", back_populates="parches")
  category = relationship("Category", back_populates="parches")
  qualifications= relationship("Qualification", back_populates="parche", cascade="all,delete")
  comments = relationship("Comment", back_populates="parche", cascade="all,delete")
  
