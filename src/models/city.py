from sqlalchemy import Column, Integer, String
from src.config.database import Base

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    pais = Column(String, index=True)
    codigo_postal = Column(String, index=True)