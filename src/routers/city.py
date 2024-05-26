from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.ciudad import City
from src.config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from src.repositories.ciudad import CityRepository

city_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@city_router.get("/", tags=['cities'], response_model=List[City], description="Returns all cities")
def get_all_cities(
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1)
    ) -> List[City]:
    db = next(get_db())
    result = CityRepository(db).get_all_cities(offset, limit)
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@city_router.get('/{id}', tags=['cities'], response_model=City, description="Returns data of one specific city")
def get_city(id: int = Path(ge=1)) -> City:
    db = next(get_db())
    element = CityRepository(db).get_city(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested city was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)

@city_router.post('/', tags=['cities'], response_model=dict, description="Creates a new city")
def create_city(city: City = Body()) -> dict:
    db = next(get_db())
    new_city = CityRepository(db).create_city(city)
    return JSONResponse(content={
        "message": "The city was successfully created",
        "data": jsonable_encoder(new_city)
    }, status_code=status.HTTP_201_CREATED)

@city_router.put('/{id}', tags=['cities'], response_model=dict, description="Updates the data of a specific city")
def update_city(id: int = Path(ge=1), city: City = Body()) -> dict:
    db = next(get_db())
    element = CityRepository(db).update_city(id, city)
    if not element:
        return JSONResponse(content={
            "message": "The requested city was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The city was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)

@city_router.delete('/{id}', tags=['cities'], response_model=dict, description="Removes a specific city")
def remove_city(id: int = Path(ge=1)) -> dict:
    db = next(get_db())
    element = CityRepository(db).delete_city(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested city was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The city was removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)
