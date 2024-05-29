from typing import List
from src.models.comment import Comment as CommentModel
from src.schemas.comment import Comment as CommentSchema

class CommentRepository():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_all_comments(self,
        offset: int, 
        limit: int
        ) -> List[CommentSchema]:
        
        query = self.db.query(CommentModel)
        if(offset is not None):
            query = query.offset(offset)
        if(limit is not None):
            query = query.limit(limit)
        return query.all()
    
    def get_comments_user(self,
        offset: int, 
        limit: int,
        idUser
        ) -> List[CommentModel]:
        
        query = self.db.query(CommentModel).filter(CommentModel.user_id == idUser)
        if(offset is not None):
            query = query.offset(offset)
        if(limit is not None):
            query = query.limit(limit)
        return query.all()
    
    def get_comments_parche(self,
        offset: int, 
        limit: int,
        idParche
        ) -> List[CommentModel]:
        
        query = self.db.query(CommentModel).filter(CommentModel.parche_id == idParche)
        if(offset is not None):
            query = query.offset(offset)
        if(limit is not None):
            query = query.limit(limit)
        return query.all()


    def get_my_comment_parche(self, idUser: int, idParche: int) -> CommentSchema:
        element = self.db.query(CommentModel).filter(CommentModel.user_id == idUser, CommentModel.parche_id == idParche).first()
        return element

    def get_comment(self, id: int) -> CommentSchema:
        element = self.db.query(CommentModel).filter(CommentModel.id == id).first()
        return element

    def create_comment(self, comment: CommentSchema) -> dict:
        new_comment = CommentModel(**comment.model_dump())
        self.db.add(new_comment)
        self.db.commit()
        self.db.refresh(new_comment)
        return new_comment
    
    def update_comment(self, id: int, comment: CommentSchema) -> dict:
        element = self.db.query(CommentModel).filter(CommentModel.id == id).first()
        element.title = comment.title
        element.content = comment.content
        element.user_id = comment.user_id
        element.parche_id = comment.parche_id
        self.db.commit()
        self.db.refresh(element)
        return element

    def update_my_comment(self, id: int,idUser:int, comment: CommentSchema) -> dict:
        element = self.db.query(CommentModel).filter(CommentModel.id == id).filter(CommentModel.user_id == idUser).first()
        element.title = comment.title
        element.content = comment.content
        element.user_id = comment.user_id
        element.parche_id = comment.parche_id
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def delete_comment(self, id: int) -> dict:
        element = self.db.query(CommentModel).filter(CommentModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element

def delete_my_comment(self, id: int, idUser: int) -> dict:
        element = self.db.query(CommentModel).filter(CommentModel.id == id).filter(CommentModel.user_id == idUser).first()
        self.db.delete(element)
        self.db.commit()
        return element