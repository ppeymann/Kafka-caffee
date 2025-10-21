from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "order_entities"
    
    id = Column(Integer, primary_key=True, index=True)
    dish_id = Column(Integer, ForeignKey("dish_entities.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customer_entities.id"), nullable=False)
    dish_id = Column(Integer, ForeignKey("dish_entities.id"), nullable=False)
    quantity = Column(Integer, default=1)
    total_price = Column(Float)
    status = Column(String, default="pentind")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    dish_rel = relationship("Dish", back_populates="orders")
    customer_rel = relationship("Customer", back_populates="orders")