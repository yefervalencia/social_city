from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler
from src.config.database import SessionLocal
from src.schemas.parche import Parche
from src.repositories.parche import ParcheRepository
from src.repositories.user import UserRepository
from src.repositories.scenery import SceneryRepository
from src.repositories.category import CategoryRepository

parche_router = APIRouter()

@parche_router.get("/",tags=['parches'],response_model=List[Parche],description="Returns all parches")
def get_all_parches(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)
        ) -> List[Parche]:
    db = SessionLocal()
    result = ParcheRepository(db).get_all_parches(offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)

@parche_router.get("/myParches",tags=['parches'],response_model=List[Parche],description="Returns all my parches")
def get_my_parches(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)
        ) -> List[Parche]:
    db = SessionLocal()
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    result = ParcheRepository(db).get_my_parches(idUser ,offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@parche_router.get("/user/{idUser}",tags=['parches'],response_model=List[Parche],description="Returns all parches of the specific user")
def get_parches_user(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)],
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        idUser: int = Path(ge=1, le=5000)
        ) -> List[Parche]:
    db = SessionLocal()
    result = ParcheRepository(db).get_parches_user(idUser,offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@parche_router.get("/scenery/{idScenery}",tags=['parches'],response_model=List[Parche],description="Returns all parches of the specific scenerey")
def get_parches_scenery(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        idScenery: int = Path(ge=1, le=5000)
        ) -> List[Parche]:
    db = SessionLocal()
    result = ParcheRepository(db).get_parches_scenery(idScenery,offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@parche_router.get("/category/{idCategory}",tags=['parches'],response_model=List[Parche],description="Returns all parches of yhe specific category")
def get_parches_category(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        idCategory: int = Path(ge=1, le=5000)
        ) -> List[Parche]:
    db = SessionLocal()
    result = ParcheRepository(db).get_parches_category(idCategory, offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@parche_router.get('/{id}',tags=['parches'],response_model=Parche,description="Returns data of one specific parche")
def get_parche(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1, le=5000)) -> Parche:
    db = SessionLocal()
    element = ParcheRepository(db).get_parche(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested parche was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)

@parche_router.post('/',tags=['parches'],response_model=dict,description="Creates a new parche")
def create_parche(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        parche: Parche = Body()) -> dict:
    db = SessionLocal()
    if not UserRepository(db).get_user_id(parche.user_id):
        raise Exception("user doesn't exist")
    if not SceneryRepository(db).get_scenery(parche.scenery_id):
        raise Exception("scenery doesn't exist")
    if not CategoryRepository(db).get_category(parche.category_id):
        raise Exception("scenery doesn't exist")
    new_parche = ParcheRepository(db).create_parche(parche)
    return JSONResponse(content={
        "message": "The parche was successfully created",
        "data": jsonable_encoder(new_parche)
    }, status_code=status.HTTP_201_CREATED)

@parche_router.put('/myParche/{id}}',tags=['parches'],response_model=dict,description="Updates the data of my parche")
def update_my_parche(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        id: int = Path(ge=1),
    parche: Parche = Body()) -> dict:
    db = SessionLocal()
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    if not UserRepository(db).get_user_id(parche.user_id):
        raise Exception("user doesn't exist")
    if not SceneryRepository(db).get_scenery(parche.parche_id):
        raise Exception("parche doesn't exist")
    if not CategoryRepository(db).get_category(parche.parche_id):
        raise Exception("parche doesn't exist")
    element = ParcheRepository(db).update_my_parche(idUser,id, parche)
    if not element:
        return JSONResponse(content={
            "message": "The requested parche was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The parche was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)
    

@parche_router.put('/{id}',tags=['parches'],response_model=dict,description="Updates the data of specific parche")
def update_parche(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1),
    parche: Parche = Body()) -> dict:
    db = SessionLocal()
    if not UserRepository(db).get_user_id(parche.user_id):
        raise Exception("user doesn't exist")
    if not SceneryRepository(db).get_scenery(parche.parche_id):
        raise Exception("parche doesn't exist")
    if not CategoryRepository(db).get_category(parche.parche_id):
        raise Exception("parche doesn't exist")
    element = ParcheRepository(db).update_parche(id, parche)
    if not element:
        return JSONResponse(content={
            "message": "The requested parche was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The parche was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)

@parche_router.delete('/myParche/{id}',tags=['parches'],response_model=dict,description="Removes my parche")
def remove_my_parche(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    element = ParcheRepository(db).delete_my__parche(idUser,id)
    if not element:
        return JSONResponse(content={
            "message": "The requested parche was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The parche wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)
    
@parche_router.delete('/{id}',tags=['parches'],response_model=dict,description="Removes specific parche")
def remove_parche(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = ParcheRepository(db).delete_parche(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested parche was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The parche wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)