from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPAuthorizationCredentials
from src.auth.has_access import security
from src.auth import auth_handler
from src.config.database import SessionLocal
from src.schemas.category import Category
from src.repositories.category import CategoryRepository

category_router = APIRouter()
    
@category_router.get("/",tags=['categories'],response_model=List[Category],description="Returns all categories")
def get_all_categories(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        offset: int = Query(default=None, min=0),
        limit: int = Query(default=None, min=1)
        ) -> List[Category]:
    db = SessionLocal()
    result = CategoryRepository(db).get_all_categories(offset,limit)
    return JSONResponse(content=jsonable_encoder(result),
    status_code=status.HTTP_200_OK)
    
@category_router.get('/{id}',tags=['categories'],response_model=Category,description="Returns data of one specific category")
def get_category(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1, le=5000)) -> Category:
    db = SessionLocal()
    element = CategoryRepository(db).get_category(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested category was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element),
    status_code=status.HTTP_200_OK)

@category_router.post('/',tags=['categories'],response_model=dict,description="Creates a new category")
def create_category(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        category: Category = Body()) -> dict:
    db = SessionLocal()
    new_category = CategoryRepository(db).create_category(category)
    return JSONResponse(content={
        "message": "The category was successfully created",
        "data": jsonable_encoder(new_category)
    }, status_code=status.HTTP_201_CREATED)

@category_router.put('/{id}',tags=['categories'],response_model=dict,description="Updates the data of specific category")
def update_category(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1),
    category: Category = Body()) -> dict:
    db = SessionLocal()
    element = CategoryRepository(db).update_category(id, category)
    if not element:
        return JSONResponse(content={
            "message": "The requested category was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The category was successfully updated",
        "data": jsonable_encoder(element)
    }, status_code=status.HTTP_200_OK)
    
@category_router.delete('/{id}',tags=['categories'],response_model=dict,description="Removes specific category")
def remove_category(credentials: Annotated[HTTPAuthorizationCredentials, 
                    Depends(security)],
        _: Annotated[None, Depends(auth_handler.verify_admin)], 
        id: int = Path(ge=1)) -> dict:
    db = SessionLocal()
    element = CategoryRepository(db).delete_category(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested category was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The category wass removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)