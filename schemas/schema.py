from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ===== Category ====
class CategoryBase(BaseModel):
    name: str
    
class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str]
    
class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        orm_mode=True

# ==== Dish ====
class DishBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    available: Optional[bool] = True
    category_id: Optional[int] = None

class DishCreate(DishBase):
    pass

class DishUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    available: Optional[bool]
    category_id: Optional[int]

class DishResponse(DishBase):
    id: int

    class Config:
        orm_mode = True
        
# ===== Customer =====
class CustomerBase(BaseModel):
    name: str
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str]
    phone: Optional[str]

class CustomerResponse(CustomerBase):
    id: int

    class Config:
        orm_mode = True

# ===== Order =====
class OrderBase(BaseModel):
    dish_id: int
    customer_id: int
    quantity: int = 1
    status: Optional[str] = "pending"

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    quantity: Optional[int]
    status: Optional[str]

class OrderResponse(OrderBase):
    id: int
    total_price: float
    created_at: datetime

    class Config:
        orm_mode = True