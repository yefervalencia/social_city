from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.config.database import Base
import datetime

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(length=100), index=True, nullable=False)
    content = Column(String(length=5000), index=True, nullable=False)
    created_at= Column(DateTime, default=datetime.datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    parche_id = Column(Integer, ForeignKey('parches.id'), nullable=False)

    user = relationship("User", back_populates="comments")
    parche = relationship("Parche", back_populates="comments")
