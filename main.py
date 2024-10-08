from fastapi import FastAPI
from src.config.database import Base, engine
from src.middlewares.error_handler import ErrorHandler
from fastapi.middleware.cors import CORSMiddleware 
from src.routers.auth import auth_router
from src.routers.category import category_router
from src.routers.city import city_router
from src.routers.comment import comment_router
from src.routers.parche import parche_router
from src.routers.qualification import qualification_router
from src.routers.scenery import scenery_router
from src.routers.user import user_router

tags_metadata = [
    {
        "name": "users",
        "description": "Users handling endpoints",  
    },
    {
        "name": "auth",
        "description": "Authentication handling endpoints",
    },
    {
        "name": "categories",
        "description": "Categories handling endpoints",
    },
    
    {
        "name": "cities",
        "description": "Cities handling endpoints",
    },
    {
        "name": "comments",
        "description": "Comments handling endpoints",
    },
    {
        "name": "parches",
        "description": "parches handling endpoints"
    },
    {
        "name": "qualifications",
        "description": "Qualifications handling endpoints",
    },
    {
        "name": "sceneries",
        "description": "Scenery handling endpoints",
    }
]

app = FastAPI(openapi_tags=tags_metadata)

app.title = "SOCIAL CITY API"
app.summary = "API REST para gestión de parches en cada ciudad de Colombia utilizando FastAPI y Python"
app.description = "This is a demonstration of API REST using Python"
app.version = "0.0.1"
app.contact = {
 "names": " yeferson valencia aristizabal",
 "url": "https://github.com/yefervalencia",
 "emails": "fabian.hernandezc@autonoma.edu.co, yeferson.valenciaa@autonoma.edu.co",
} 

Base.metadata.create_all(bind=engine)

app.add_middleware(ErrorHandler)

# Configurar CORS
origins = [
    "http://localhost",  # URL de tu frontend local
    "http://localhost:3000",  # Otra URL común para el frontend
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir orígenes específicos
    allow_credentials=True,  # Permitir uso de cookies
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los headers
)

app.include_router(prefix="", router=auth_router)
app.include_router(prefix="/users", router=user_router)
app.include_router(prefix="/categories", router=category_router)
app.include_router(prefix="/cities", router=city_router)
app.include_router(prefix="/comments", router=comment_router)
app.include_router(prefix="/parches", router=parche_router)
app.include_router(prefix="/qualifications", router=qualification_router)
app.include_router(prefix="/sceneries", router=scenery_router)