from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from src.config.database import Base

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  email = Column(String(length=64), unique=True, index=True)
  name = Column(String(length=60))
  password = Column(String(length=64))
  is_active = Column(Boolean, default=True)
  
  expenses = relationship("Expense", back_populates="owner")
  incomes = relationship("Income", back_populates="owner")
  reports = relationship("Report", back_populates="owner")