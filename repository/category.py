from sqlalchemy.orm import Session
from .base import BaseRepository
from models.category import Category

class CategoryRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(Category, db)