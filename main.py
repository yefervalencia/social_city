from src.routers.user import user_router
from src.middlewares.errror_handler import ErrorHandler
from fastapi import FastAPI
from src.config.database import Base, engine
from src.routers.auth import auth_router

tags_metadata = [
    {
        "name": "usuarios",
        "description": "Users handling endpoints",  
    },
    {
        "name": "auth",
        "description": "User's authentication",
    },
    {
        "name": "i",
        "description": "User's incomes",
    },
    {
        "name": "expenses",
        "description": "User's expenses",
    },
    {
        "name": "reports",
        "description": "User's reports of incomes and expenses",
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

 