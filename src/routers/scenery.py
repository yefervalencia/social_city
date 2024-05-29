from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler
from src.config.database import SessionLocal
from src.schemas.scenery import Scenery
from src.repositories.scenery import SceneryRepository
from src.repositories.city import CityRepository

scenery_router = APIRouter()

@scenery_router.get("/",tags=['sceneries'],response_model=List[Scenery],description="Returns all sceneries")
def get_all_sceneries(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)
        ) -> List[Scenery]:
    db = SessionLocal()
    result = SceneryRepository(db).get_all_sceneries(offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@scenery_router.get('/{id}',tags=['sceneries'],response_model=Scenery,description="Returns data of one specific scenery")
def get_scenery(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        id: int = Path(ge=1, le=5000)) -> Scenery:
    db = SessionLocal()
    element = SceneryRepository(db).get_scenery(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested scenery was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)
    
@scenery_router.get('/city/{idCity}',tags=['sceneries'],response_model=List[Scenery],description="Returns data of scenerie in specific city")
def get_sceneries_city(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        idCity: int = Path(ge=1, le=5000)) -> List[Scenery]:
    db = SessionLocal()
    result = SceneryRepository(db).get_sceneries_city(offset, limit, idCity)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)

@scenery_router.post('/',tags=['sceneries'],response_model=dict,description="Creates a new scenery")
def create_scenery(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        scenery: Scenery = Body()) -> dict:
    db = SessionLocal()
    if not CityRepository(db).get_city(scenery.city_id):
        raise Exception("city doesn't exist")
    
    new_scenery = SceneryRepository(db).create_scenery(scenery)
    return JSONResponse(content={
        "message": "The scenery was successfully created",
        "data": jsonable_encoder(new_scenery)
    }, status_code=status.HTTP_201_CREATED)

@scenery_router.put('/{id}',tags=['sceneries'],response_model=dict,description="Updates the data of specific scenery")
def update_scenery(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1),
    scenery: Scenery = Body()) -> dict:
    db = SessionLocal()
    if not CityRepository(db).get_city(scenery.city_id):
        raise Exception("city doesn't exist")
    element = SceneryRepository(db).update_scenery(id, scenery)
    if not element:
        return JSONResponse(content={
            "message": "The requested scenery was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The scenery was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)
    
@scenery_router.delete('/{id}',tags=['sceneries'],response_model=dict,description="Removes specific scenery")
def remove_scenery(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = SceneryRepository(db).delete_scenery(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested scenery was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The scenery wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)