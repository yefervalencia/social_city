import jwt
from fastapi import APIRouter, Body, Query, Path, status, Depends,HTTPException
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from src.auth import auth_handler
from src.auth.has_access import security
from src.config.database import SessionLocal
from src.schemas.user import User
from src.repositories.user import UserRepository

user_router = APIRouter()

def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, auth_handler.secret, algorithms=[auth_handler.algorithm])
        rol: str = payload.get("user.rol")
        if rol is None:
            raise credentials_exception
        if rol != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except jwt.InvalidSignatureError:
        raise credentials_exception
    return token

@user_router.get("/",tags=['users'],response_model=List[User],description="Returns all users")
def get_all_users(
        credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1),
        ) -> List[User]:
    db = SessionLocal()
    result = UserRepository(db).get_all_users(offset,limit)
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
        _: Annotated[None, Depends(verify_admin)], 
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
        _: Annotated[None, Depends(verify_admin)], 
        id: int = Path(ge=1),
        user: User = Body()) -> dict:
    db = SessionLocal()
    element = UserRepository(db).update_user(id, user)
    if not element:
        return JSONResponse(content={
            "message": "The requested user was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The user was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)


@user_router.delete('/myuser',tags=['users'],response_model=dict,description="Removes my user")
def remove_user(credentials: Annotated[HTTPAuthorizationCredentials, 
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
def remove_user(id: int = Path(ge=1)) -> dict:
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
