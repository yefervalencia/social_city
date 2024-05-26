from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.comment import Comment
from src.config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from src.repositories.comment import CommentRepository

comment_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@comment_router.get("/", tags=['comments'], response_model=List[Comment], description="Returns all comments")
def get_all_comments(
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1)
    ) -> List[Comment]:
    db = next(get_db())
    result = CommentRepository(db).get_all_comments(offset, limit)
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@comment_router.get('/{id}', tags=['comments'], response_model=Comment, description="Returns data of one specific comment")
def get_comment(id: int = Path(ge=1)) -> Comment:
    db = next(get_db())
    element = CommentRepository(db).get_comment(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested comment was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)

@comment_router.post('/', tags=['comments'], response_model=dict, description="Creates a new comment")
def create_comment(comment: Comment = Body()) -> dict:
    db = next(get_db())
    new_comment = CommentRepository(db).create_comment(comment)
    return JSONResponse(content={
        "message": "The comment was successfully created",
        "data": jsonable_encoder(new_comment)
    }, status_code=status.HTTP_201_CREATED)

@comment_router.put('/{id}', tags=['comments'], response_model=dict, description="Updates the data of a specific comment")
def update_comment(id: int = Path(ge=1), comment: Comment = Body()) -> dict:
    db = next(get_db())
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

@comment_router.delete('/{id}', tags=['comments'], response_model=dict, description="Removes a specific comment")
def remove_comment(id: int = Path(ge=1)) -> dict:
    db = next(get_db())
    element = CommentRepository(db).delete_comment(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested comment was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The comment was removed successfully",
        "data": None
    }, status_code=status.HTTP_200_OK)
