from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler
from src.config.database import SessionLocal
from src.repositories.city import CityRepository
from src.schemas.city import City
from src.repositories.user import UserRepository

city_router = APIRouter()

@city_router.get("/",tags=['cities'],response_model=List[City],description="Returns all cities")
def get_all_cities(
        credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)
        ) -> List[City]:
    db = SessionLocal()
    result = CityRepository(db).get_all_cities(offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@city_router.get('/myCity',tags=['cities'],response_model=City,description="Returns data of one specific city")
def get_my_city(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)]) -> City:
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        email = payload.get("sub")
    db = SessionLocal()
    current_user = UserRepository(db).get_user(email)
    element = CityRepository(db).get_city(current_user.city_id)
    if not element:
        return JSONResponse(content={
            "message": "The requested city was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)
    
@city_router.get('/{id}',tags=['cities'],response_model=City,description="Returns data of one specific city")
def get_city(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
    id: int = Path(ge=1, le=5000)) -> City:
    db = SessionLocal()
    element = CityRepository(db).get_city(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested city was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)

@city_router.post('/',tags=['cities'],response_model=dict,description="Creates a new city")
def create_city(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
    city: City = Body()) -> dict:
    db = SessionLocal()
    new_city = CityRepository(db).create_city(city)
    return JSONResponse(content={
        "message": "The city was successfully created",
        "data": jsonable_encoder(new_city)
    }, status_code=status.HTTP_201_CREATED)

@city_router.put('/{id}',tags=['cities'],response_model=dict,description="Updates the data of specific city")
def update_city(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
    id: int = Path(ge=1),
    city: City = Body()) -> dict:
    db = SessionLocal()
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
    
@city_router.delete('/{id}',tags=['cities'],response_model=dict,description="Removes specific city")
def remove_city(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
    id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = CityRepository(db).delete_city(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested city was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The city wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)