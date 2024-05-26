from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List
from src.schemas.qualification import Qualification
from src.config.database import SessionLocal
from fastapi.encoders import jsonable_encoder
from src.repositories.qualification import QualificationRepository

qualification_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@qualification_router.get("/", tags=['qualifications'], response_model=List[Qualification], description="Returns all qualifications")
def get_all_qualifications(
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1)
    ) -> List[Qualification]:
    db = next(get_db())
    result = QualificationRepository(db).get_all_qualifications(offset, limit)
    return JSONResponse(content=jsonable_encoder(result), status_code=status.HTTP_200_OK)

@qualification_router.get('/{id}', tags=['qualifications'], response_model=Qualification, description="Returns data of one specific qualification")
def get_qualification(id: int = Path(ge=1)) -> Qualification:
    db = next(get_db())
    element = QualificationRepository(db).get_qualification(id)
    if not element:
        return JSONResponse(content={
            "message": "The requested qualification was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(element), status_code=status.HTTP_200_OK)

@qualification_router.post('/', tags=['qualifications'], response_model=dict, description="Creates a new qualification")
def create_qualification(qualification: Qualification = Body()) -> dict:
    db = next(get_db())
    new_qualification = QualificationRepository(db).create_qualification(qualification)
    return JSONResponse(content={
        "message": "The qualification was successfully created",
        "data": jsonable_encoder(new_qualification)
    }, status_code=status.HTTP_201_CREATED)

@qualification_router.put('/{id}', tags=['qualifications'], response_model=dict, description="Updates the data of a specific qualification")
def update_qualification(id: int = Path(ge=1), qualification: Qualification = Body()) -> dict:
    db = next(get_db())
    element = QualificationRepository(db).update_qualification(id, qualification)
    if not element:
        return JSONResponse(content={
            "message": "The requested qualification was not found",
            "data": None
        }, status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content={
        "message": "The qualification was successfully updated",
        "data": jsonable
    })