from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler
from src.config.database import SessionLocal
from src.schemas.qualification import Qualification
from src.repositories.qualification import QualificationRepository
from src.repositories.user import UserRepository
from src.repositories.parche import ParcheRepository

qualification_router = APIRouter()

@qualification_router.get("/",tags=['qualifications'],response_model=List[Qualification],description="Returns all qualifications")
def get_all_qualifications(
    credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)
        ) -> List[Qualification]:
    db = SessionLocal()
    result = QualificationRepository(db).get_all_qualifications(offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@qualification_router.get('/myQualifications',tags=['qualifications'],response_model=List[Qualification],description="Returns data of qualifications of my user")
def get_my_qualifications(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)) -> List[Qualification]:
    db = SessionLocal()
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    result = QualificationRepository(db).get_qualifications_user(offset, limit, idUser)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@qualification_router.get('/user/{idUser}',tags=['qualifications'],response_model=List[Qualification],description="Returns data of qualifications of a specific user")
def get_qualifications_user(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        idUser: int = Path(ge=1, le=5000)) -> List[Qualification]:
    db = SessionLocal()
    result = QualificationRepository(db).get_qualifications_user(offset, limit, idUser)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@qualification_router.get('/parche/{idParche}',tags=['qualifications'],response_model=List[Qualification],description="Returns data of qualifications of a specific parche")
def get_qualifications_parche(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        idParche: int = Path(ge=1, le=5000)) -> List[Qualification]:
    db = SessionLocal()
    result = QualificationRepository(db).get_qualifications_parche(offset, limit, idParche)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@qualification_router.get('/{id}',tags=['qualifications'],response_model=Qualification,description="Returns data of one specific qualification")
def get_qualification(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1, le=5000)) -> Qualification:
    db = SessionLocal()
    element = QualificationRepository(db).get_qualification(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested qualification was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)
    
@qualification_router.get('/myQualification/{idParche}',tags=['qualifications'],response_model=Qualification,description="Returns data of my qualification in a specific parche")
def get_my_qualification_parche(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        idParche: int = Path(ge=1, le=5000)) -> Qualification:
    db = SessionLocal()
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    element = QualificationRepository(db).get_my_comment_parche(idUser,idParche)
    if not element:
        return JSONResponse(content={
            "message": "The requested comment was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)

@qualification_router.post('/',tags=['qualifications'],response_model=dict,description="Creates a new qualification")
def create_qualification(
    credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)], 
        qualification: Qualification = Body()) -> dict:
    db = SessionLocal()
    if not UserRepository(db).get_user_id(qualification.user_id):
        raise Exception("user doesn't exist")
    if not ParcheRepository(db).get_parche(qualification.parche_id):
        raise Exception("parche doesn't exist")
    new_qualification = QualificationRepository(db).create_qualification(qualification)
    return JSONResponse(content={
        "message": "The qualification was successfully created",
        "data": jsonable_encoder(new_qualification)
    }, status_code=status.HTTP_201_CREATED)

@qualification_router.put('/myQualification/{id}',tags=['qualifications'],response_model=dict,description="Updates the data of my qualification")
def update_my_qualification(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
                    id: int = Path(ge=1),
    qualification: Qualification = Body()) -> dict:
    db = SessionLocal()
    if not UserRepository(db).get_user_id(qualification.user_id):
        raise Exception("user doesn't exist")
    if not ParcheRepository(db).get_parche(qualification.parche_id):
        raise Exception("parche doesn't exist")
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    element = QualificationRepository(db).update_my_qualification(id,idUser, qualification)
    if not element:
        return JSONResponse(content={
            "message": "The requested qualification was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The qualification was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)

@qualification_router.put('/{id}',tags=['qualifications'],response_model=dict,description="Updates the data of specific qualification")
def update_qualification(
    credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1),
    qualification: Qualification = Body()) -> dict:
    db = SessionLocal()
    if not UserRepository(db).get_user_id(qualification.user_id):
        raise Exception("user doesn't exist")
    if not ParcheRepository(db).get_parche(qualification.parche_id):
        raise Exception("parche doesn't exist")
    token = credentials.credentials
    element = QualificationRepository(db).update_qualification(id, qualification)
    if not element:
        return JSONResponse(content={
            "message": "The requested qualification was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The qualification was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)
    
@qualification_router.delete('/myQualification/{id}',tags=['qualifications'],response_model=dict,description="Removes specific qualification")
def remove_my_qualification(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
    id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    element = QualificationRepository(db).delete_my_qualification(id,idUser)
    if not element:
        return JSONResponse(content={
            "message": "The requested qualification was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The qualification wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)

@qualification_router.delete('/{id}',tags=['qualifications'],response_model=dict,description="Removes specific qualification")
def remove_qualification(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
    id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = QualificationRepository(db).delete_qualification(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested qualification was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The qualification wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)