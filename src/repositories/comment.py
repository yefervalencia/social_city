from fastapi import APIRouter, Body, Query, Path, status, Depends
from fastapi.responses import JSONResponse
from typing import List, Annotated
from sqlalchemy.orm import Session
from src.models.comment import Comment as CommentModel
from src.schemas.comment import Comment as CommentSchema

class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

def get_all_comments(self, offset: int = 0, limit: int = 10):
        return self.db.query(CommentModel).offset(offset).limit(limit).all()

def get_comment(self, comment_id: int):
        return self.db.query(CommentModel).filter(CommentModel.id == comment_id).first()

def create_comment(self, comment: CommentSchema):
        db_comment = CommentModel(
            content=comment.content,
            user_id=comment.user_id,
            city_id=comment.city_id
        )
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment

def update_comment(self, comment_id: int, comment: CommentSchema):
        db_comment = self.get_comment(comment_id)
        if db_comment:
            db_comment.content = comment.content
            db_comment.user_id = comment.user_id
            db_comment.city_id = comment.city_id
            self.db.commit()
            self.db.refresh(db_comment)
        return db_comment

def delete_comment(self, comment_id: int):
        db_comment = self.get_comment(comment_id)
        if db_comment:
            self.db.delete(db_comment)
            self.db.commit()
        return db_comment
