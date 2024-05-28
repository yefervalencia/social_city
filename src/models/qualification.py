from sqlalchemy import Column, Integer, ForeignKey, DateTime,Float
from sqlalchemy.orm import relationship
from src.config.database import Base
import datetime

class Qualification(Base):
    __tablename__ = "qualifications"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, nullable=False)
    created_at= Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    parche_id = Column(Integer, ForeignKey('parches.id'))

    user = relationship("User", back_populates="qualifications")
    parche = relationship("Parche", back_populates="qualifications")
