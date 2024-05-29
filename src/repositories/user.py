from typing import List
from src.models.user import User as UserModel
from src.schemas.user import User as UserSchema

class UserRepository():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_all_users(self,
        offset: int, 
        limit: int
        ) -> List[UserSchema]:
        
        query = self.db.query(UserModel)
        if(offset is not None):
            query = query.offset(offset)
        if(limit is not None):
            query = query.limit(limit)
        return query.all()

    def get_user(self, email: str) -> UserSchema:
        element = self.db.query(UserModel).filter(UserModel.email == email).first()
        return element
    

    def create_user(self, user: UserSchema) -> dict:
        new_user = UserModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
    
    def update_user(self, id: int, user: UserSchema) -> dict:
        element = self.db.query(UserModel).filter(UserModel.id == id).first()
        #hashed_password = auth_handler.hash_password(password=user.password)
        element.name=user.name,
        element.lastname=user.lastname,
        element.email=user.email,
        #element.password=hashed_password,
        element.rol=user.rol,
        element.is_active=user.is_active,
        element.born_date=user.born_date,
        element.cellphone=user.cellphone,
        element.city_id=user.city_id
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def delete_user(self, id: int) -> dict:
        element = self.db.query(UserModel).filter(UserModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element