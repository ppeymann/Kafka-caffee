from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, model, db: Session) -> None:
        self.model = model
        self.db = db
    
    def get(self, id: int):
        return self.db.query(self.model).filter(self.model.id==id).first()

    def get_by(self, **kwargs):
        return self.db.query(self.model).filter_by(**kwargs).first()
    
    def get_all(self):
        return self.db.query(self.model).all()
    
    def create(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj
    
    def delete(self, id: int):
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj