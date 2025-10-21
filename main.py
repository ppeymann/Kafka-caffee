from fastapi import FastAPI
from core.database import Base, engine
from api import category
from models.customer import Customer
from models.dish import Dish
from models.order import Order

# creating tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Resturant API", version="1.0")

app.include_router(category.router)

# this api is for check api health
@app.get("/health")
def health_check():
    return {"status": "OK", "message":"Resturant API is running 🍽️"}