from sqlalchemy import Boolean, Column, Integer, String
from src.config.database import Base

class Admin(Base):
  __tablename__ = "admins"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(length=40), index=True, nullable=False)
  email = Column(String(Length=40), unique=True, nullable=False)
  password = Column(String, nullable=False)
  is_active = Column(Boolean, default=True)