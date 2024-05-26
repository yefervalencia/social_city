from fastapi import FastAPI
from src.config.database import Base, engine
from src.middlewares.errror_handler import ErrorHandler
from src.routers.auth import auth_router
from src.routers.user import user_router
from src.routers.city import city_router
from src.routers.comment import comment_router

tags_metadata = [
    {
        "name": "users",
        "description": "Users handling endpoints",  
    },
    {
        "name": "auth",
        "description": "User's authentication",
    },
    {
        "name": "city",
        "description": "User's city",
    },
    {
        "name": "comments",
        "description": "User's comments",
    },
    {
        "name": "quialification",
        "description": "User's qualification",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

app.title = "SOCIAL CITY API"
app.summary = "API REST para gestión de parches en Colombia utilizando FastAPI y Python"
app.description = "This is a demonstration of API REST using Python"
app.version = "0.0.1"
app.contact = {
 "names": "Fabian Hernandez Castano, yeferson valencia aristizabal",
 "url": "https://github.com/faberh12",
 "emails": "fabian.hernandezc@autonoma.edu.co, yeferson.valenciaa@autonoma.edu.co",
} 

Base.metadata.create_all(bind=engine)

app.add_middleware(ErrorHandler)

app.include_router(prefix="", router=auth_router)
app.include_router(prefix="/users", router=user_router)
app.include_router(prefix="/cities", router=city_router)
app.include_router(prefix="/comments", router=comment_router)

 