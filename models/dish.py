from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database import Base

class Dish(Base):
    __tablename__ = "dish_entities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    avalible = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("category_entities.id"))
    
    category_rel = relationship("Category", back_populates="dishes")
    orders = relationship("Order", back_populates="dish_rel")

