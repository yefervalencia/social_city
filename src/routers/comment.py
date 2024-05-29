from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler
from src.config.database import SessionLocal
from src.schemas.comment import Comment
from src.repositories.comment import CommentRepository
from src.repositories.user import UserRepository
from src.repositories.parche import ParcheRepository

comment_router = APIRouter()

@comment_router.get("/",tags=['comments'],response_model=List[Comment],description="Returns all comments")
def get_all_comments(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)
        ) -> List[Comment]:
    db = SessionLocal()
    result = CommentRepository(db).get_all_comments(offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@comment_router.get('/myComments',tags=['comments'],response_model=List[Comment],description="Returns data of comments of my user")
def get_my_comments(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)) -> List[Comment]:
    db = SessionLocal()
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    result = CommentRepository(db).get_comments_user(offset, limit, idUser)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@comment_router.get('/user/{idUser}',tags=['comments'],response_model=List[Comment],description="Returns data of comments of a specific user")
def get_comments_user(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        idUser: int = Path(ge=1, le=5000)) -> List[Comment]:
    db = SessionLocal()
    result = CommentRepository(db).get_comments_user(offset, limit, idUser)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@comment_router.get('/parche/{idParche}',tags=['comments'],response_model=List[Comment],description="Returns data of qualifications of a specific parche")
def get_comments_parche(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        idParche: int = Path(ge=1, le=5000)) -> List[Comment]:
    db = SessionLocal()
    result = CommentRepository(db).get_comments_parche(offset, limit, idParche)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@comment_router.get('/{id}',tags=['comments'],response_model=Comment,description="Returns data of one specific comment")
def get_comment(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1, le=5000)) -> Comment:
    db = SessionLocal()
    element = CommentRepository(db).get_comment(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested comment was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)

@comment_router.get('/myComment/{idParche}',tags=['comments'],response_model=Comment,description="Returns data of my comment in a specific parche")
def get_my_comment_parche(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        idParche: int = Path(ge=1, le=5000)) -> Comment:
    db = SessionLocal()
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    element = CommentRepository(db).get_my_comment_parche(idUser,idParche)
    if not element:
        return JSONResponse(content={
            "message": "The requested comment was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)

@comment_router.post('/',tags=['comments'],response_model=dict,description="Creates a new comment")
def create_comment(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
                    comment: Comment = Body()) -> dict:
    db = SessionLocal()
    if not UserRepository(db).get_user_id(comment.user_id):
        raise Exception("user doesn't exist")
    if not ParcheRepository(db).get_parche(comment.parche_id):
        raise Exception("parche doesn't exist")
    token = credentials.credentials
    new_comment = CommentRepository(db).create_comment(comment)
    return JSONResponse(content={
        "message": "The comment was successfully created",
        "data": jsonable_encoder(new_comment)
    }, status_code=status.HTTP_201_CREATED)

@comment_router.put('/myComment/{id}',tags=['comments'],response_model=dict,description="Updates the data of specific comment")
def update_my_comment(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)], 
        id: int = Path(ge=1),
        comment: Comment = Body()) -> dict:
    db = SessionLocal()
    if not UserRepository(db).get_user_id(comment.user_id):
        raise Exception("user doesn't exist")
    if not ParcheRepository(db).get_parche(comment.parche_id):
        raise Exception("parche doesn't exist")
    token = credentials.credentials
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    element = CommentRepository(db).update_my_omment(id,idUser, comment)
    if not element:
        return JSONResponse(content={
            "message": "The requested comment was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The comment was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)

@comment_router.put('/{id}',tags=['comments'],response_model=dict,description="Updates the data of specific comment")
def update_comment(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1),
    comment: Comment = Body()) -> dict:
    db = SessionLocal()
    if not UserRepository(db).get_user_id(comment.user_id):
        raise Exception("user doesn't exist")
    if not ParcheRepository(db).get_parche(comment.parche_id):
        raise Exception("parche doesn't exist")
    token = credentials.credentials
    element = CommentRepository(db).update_comment(id, comment)
    if not element:
        return JSONResponse(content={
            "message": "The requested comment was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The comment was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)
    
@comment_router.delete('/myComment/{id}',tags=['comments'],response_model=dict,description="Removes specific comment")
def remove_my_comment(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
                    id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    token = credentials.credentials
    payload = auth_handler.decode_token(token=token)
    if payload:
        idUser = payload.get("user.id")
    element = CommentRepository(db).delete_my_comment(id,idUser)
    if not element:
        return JSONResponse(content={
            "message": "The requested comment was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The comment wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)

@comment_router.delete('/{id}',tags=['comments'],response_model=dict,description="Removes specific comment")
def remove_comment(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = CommentRepository(db).delete_comment(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested comment was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The comment wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)