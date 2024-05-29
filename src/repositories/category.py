from typing import List
from src.models.category import Category as CategoryModel
from src.schemas.category import Category as CategorySchema

class CategoryRepository():
    def __init__(self, db) -> None:
        self.db = db
        
    def get_all_categories(self,
        offset: int, 
        limit: int
        ) -> List[CategorySchema]:
        
        query = self.db.query(CategoryModel)
        if(offset is not None):
            query = query.offset(offset)
        if(limit is not None):
            query = query.limit(limit)
        return query.all()

    def get_category(self, id: int) -> CategorySchema:
        element = self.db.query(CategoryModel).filter(CategoryModel.id == id).first()
        return element

    def create_category(self, category: CategorySchema) -> dict:
        new_category = CategoryModel(**category.model_dump())
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category
    
    def update_category(self, id: int, category: CategorySchema) -> dict:
        element = self.db.query(CategoryModel).filter(CategoryModel.id == id).first()
        element.name = category.name
        element.description = category.description
        self.db.commit()
        self.db.refresh(element)
        return element
    
    def delete_category(self, id: int) -> dict:
        element = self.db.query(CategoryModel).filter(CategoryModel.id == id).first()
        self.db.delete(element)
        self.db.commit()
        return element