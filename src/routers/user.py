from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials
from src.auth import auth_handler
from src.auth.has_access import security
from src.config.database import SessionLocal
from src.schemas.user import User
from src.repositories.user import UserRepository
from src.repositories.city import CityRepository

user_router = APIRouter()

@user_router.get("/",tags=['users'],response_model=List[User],description="Returns all users")
def get_all_users(
        credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        ) -> List[User]:
    db = SessionLocal()
    result = UserRepository(db).get_all_users(offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@user_router.get('/city/{idCity}',tags=['users'],response_model=List[User],description="Returns data of user in specific city")
def get_users_city(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        idCity: int = Path(ge=1, le=5000)) -> List[User]:
    db = SessionLocal()
    result = UserRepository(db).get_users_city(offset, limit, idCity)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@user_router.get('/myUser',tags=['users'],response_model=User,description="Returns data of my user")
def get_my_user(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)]) -> User:
    token = credentials.credentials
    
    payload = auth_handler.decode_token(token=token)

    if payload:
        email = payload.get("sub")
    
    db = SessionLocal()
    element = UserRepository(db).get_user(email)
    if not element:
        return JSONResponse(content={
            "message": "The requested user was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)
    
@user_router.get('/{email}',tags=['users'],response_model=User,description="Returns data of one specific user")
def get_user(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        email: str = Path()) -> User:
    print("falla")
    db = SessionLocal()
    element = UserRepository(db).get_user(email)
    if not element:
        return JSONResponse(content={
            "message": "The requested user was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)

@user_router.put('/myUser',tags=['users'],response_model=dict,description="Updates the data of my user")
def update_my_user(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        user: User = Body()) -> dict:
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        issue = payload.get("user.id")
    db = SessionLocal()
    element = UserRepository(db).update_user(issue, user)
    if not CityRepository(db).get_city(user.city_id):
        raise Exception("city doesn't exist")
    if not element:
        return JSONResponse(content={
            "message": "The requested user was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The user was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)    

@user_router.put('/{id}',tags=['users'],response_model=dict,description="Updates the data of specific user")
def update_user(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1),
        user: User = Body()) -> dict:
    db = SessionLocal()
    element = UserRepository(db).update_user(id, user)
    if not CityRepository(db).get_city(user.city_id):
        raise Exception("city doesn't exist")
    if not element:
        return JSONResponse(content={
            "message": "The requested user was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The user was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)


@user_router.delete('/myUser',tags=['users'],response_model=dict,description="Removes my user")
def remove_my_user(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)]) -> dict:
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        issue = payload.get("user.id")
    db = SessionLocal()
    element = UserRepository(db).delete_user(issue)
    if not element:
        return JSONResponse(content={
            "message": "The requested user was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The user wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)
    
@user_router.delete('/{id}',tags=['users'],response_model=dict,description="Removes specific user")
def remove_user(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)],
        id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = UserRepository(db).delete_user(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested user was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The user wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)
