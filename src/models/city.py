from sqlalchemy import Column, Integer, String
from src.config.database import Base
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String, index=True, unique=True, nullable=False)
    country = Column(String, nullable=False)
    zip = Column(String(length=6), index=True, nullable=False)

    users = relationship("User", back_populates="city")
    sceneries = relationship("Scenery", back_populates="city")
