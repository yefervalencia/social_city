from sqlalchemy.orm import Session
from src.models.city import City as CityModel
from src.schemas.city import City as CitySchema

class CityRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_cities(self, offset: int = 0, limit: int = 10):
        return self.db.query(CityModel).offset(offset).limit(limit).all()

    def get_city(self, city_id: int):
        return self.db.query(CityModel).filter(CityModel.id == city_id).first()

    def create_city(self, city: CitySchema):
        db_city = CityModel(
            nombre=city.nombre,
            pais=city.pais,
            codigo_postal=city.codigo_postal
        )
        self.db.add(db_city)
        self.db.commit()
        self.db.refresh(db_city)
        return db_city

    def update_city(self, city_id: int, city: CitySchema):
        db_city = self.get_city(city_id)
        if db_city:
            for var, value in vars(city).items():
                setattr(db_city, var, value) if value else None
            self.db.commit()
            self.db.refresh(db_city)
        return db_city

    def delete_city(self, city_id: int):
        db_city = self.get_city(city_id)
        if db_city:
            self.db.delete(db_city)
            self.db.commit()
        return db_city
