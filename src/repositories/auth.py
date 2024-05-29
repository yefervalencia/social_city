from fastapi import HTTPException, status
from src.repositories.user import UserRepository
from src.config.database import SessionLocal
from src.auth import auth_handler
from src.schemas.user import UserLogin as UserLoginSchema
from src.schemas.user import User as UserSchema
from src.repositories.city import CityRepository

class AuthRepository:
    def __init__(self) -> None:
        pass

    def register_user(self,
        user: UserSchema) -> dict:
        db = SessionLocal()
        if UserRepository(db).get_user(email=user.email) != None:
            raise Exception("Account already exists")
        if not CityRepository(db).get_city(user.city_id):
            raise Exception("city doesn't exist")
        
        
        hashed_password = auth_handler.hash_password(password=user.password)
        new_user: UserSchema = UserSchema(
            name=user.name,
            lastname=user.lastname,
            email=user.email,
            password=hashed_password,
            rol=user.rol,
            is_active=user.is_active,
            born_date=user.born_date,
            cellphone=user.cellphone,
            city_id=user.city_id
        )
        return UserRepository(db).create_user(new_user)

    def login_user(self, user: UserLoginSchema) -> dict:
        db = SessionLocal()
        check_user = UserRepository(db).get_user(email=user.email)
        if check_user is None:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials (email)",
            )
        if not check_user.is_active:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The user is not allowed to log in",
            )

        if not auth_handler.verify_password(user.password, check_user.password):
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials (password)",
            )

        access_token = auth_handler.encode_token(check_user)
        refresh_token = auth_handler.encode_refresh_token(check_user)
        return access_token, refresh_token