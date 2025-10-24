from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Pydantic v2: جایگزین orm_mode