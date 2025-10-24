from sqlalchemy.orm import Session
from .base import BaseRepository
from models.auth import User

class AuthRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(User, db)