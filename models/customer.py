from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database import Base

class Customer(Base):
    __tablename__ = "customer_entities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    phone = Column(String, unique=True, index=True)
    
    orders = relationship("Order", back_populates="customer_rel")
    
    