import os
from datetime import timedelta, datetime

from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def hashed_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]
    return bcrypt_context.hash(password_bytes)


def create_token(id: int) -> str:
    return jwt.encode(
        {"sub": str(id), "exp": datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],options={"verify_exp": True})

        return payload
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="p Denied")