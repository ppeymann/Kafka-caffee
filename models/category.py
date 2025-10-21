from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database import Base

class Category(Base):
    __tablename__ = "category_entities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    dishes = relationship("Dish", back_populates="category_rel")
    
    