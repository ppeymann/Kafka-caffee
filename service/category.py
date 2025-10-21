from repository.category import CategoryRepository
from schemas.schema import CategoryCreate, CategoryUpdate

class CategoryService:
    def __init__(self, repo: CategoryRepository) -> None:
        self.repo = repo
        
    def create_category(self, data: CategoryCreate):
        category = self.repo.model(name=data.name)
        return self.repo.create(category)
    
    def update_category(self, id:int, data: CategoryUpdate):
        category = self.repo.get(id)
        if not category:
            return None
        if data.name is not None:
            category.name = data.name
        return self.repo.create(category)
        