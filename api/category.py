from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from service.category import CategoryService
from repository.category import CategoryRepository
from schemas.schema import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("/", response_model=CategoryResponse)
def create_category(data: CategoryCreate, db: Session=Depends(get_db)):
    repo = CategoryRepository(db)
    service = CategoryService(repo)
    return service.create_category(data)

@router.get("/", response_model=list[CategoryResponse])
def get_category(db: Session=Depends(get_db)):
    repo = CategoryRepository(db)
    return repo.get_all()