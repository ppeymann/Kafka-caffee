from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from core.database import get_db
from repository.auth import AuthRepository
from schemas.auth import UserCreate
from utils.utils import (
    hashed_password,
    SECRET_KEY,
    ALGORITHM,
    bcrypt_context,
    create_token,
    decode_token
)
from models.auth import User
from jose import jwt, JWTError
from starlette import status


class AuthService:
    """
    Service layer responsible for user authentication and authorization logic.
    This class encapsulates user creation, login, and token verification logic,
    separating business rules from route definitions.
    """

    def __init__(self, repo: AuthRepository) -> None:
        """
        Initialize AuthService with a dependency-injected AuthRepository.
        :param repo: AuthRepository instance handling DB operations.
        """
        self.repo = repo

    def create_user(self, data: UserCreate):
        """
        Create a new user and issue a JWT token upon successful registration.
        Steps:
            1. Check if the username already exists.
            2. Hash the provided password.
            3. Persist the user in the database.
            4. Generate an access token.
        :param data: UserCreate schema containing username and password.
        :return: JWT token payload (dict) or False if user already exists.
        """
        # Build a new user object with hashed password
        user = self.repo.model(username=data.username, hashed_password=hashed_password(data.password))

        # Prevent duplicate usernames
        exist_user = self.repo.get_by(username=data.username)
        if exist_user:
            return False

        # Persist user in the database
        new_user = self.repo.create(user)

        # Generate JWT token for authentication
        token = create_token(new_user.id)

        # Return token and type as a standardized response
        return {
            "access_token": token,
            "token_type": "bearer",
        }

    def login(self, data: UserCreate):
        """
        Authenticate a user based on credentials and return an access token.
        Steps:
            1. Retrieve user from the database by username.
            2. Verify the password using bcrypt.
            3. Generate and return a new JWT token upon successful authentication.
        :param data: UserCreate schema with username and password.
        :return: JWT token payload (dict) or False if authentication fails.
        """
        # Retrieve user record
        user: User = self.repo.get_by(username=data.username)
        if not user:
            return False

        # Validate password against stored hash
        if not bcrypt_context.verify(data.password, user.hashed_password):
            return False

        # Create JWT token for authenticated user
        token = create_token(user.id)

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    def me(self, token: str):
        """
        Decode and validate a JWT token to retrieve the current user's profile.
        Steps:
            1. Decode the provided token.
            2. Extract user ID ('sub') from token payload.
            3. Retrieve corresponding user record from the database.
        :param token: JWT access token (Bearer token).
        :return: User instance or raise 401 if token is invalid.
        """
        try:
            # Decode token and extract payload
            payload = decode_token(token)
            id = payload.get("sub")
            if not id:
                return False

            # Retrieve user by ID from DB
            user = self.repo.get(id=id)
            if not user:
                return False

            return user

        except JWTError:
            # Handle invalid, expired, or tampered tokens
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token. Access denied."
            )


def get_auth_service(db: Session = Depends(get_db)):
    """
    FastAPI dependency injection for AuthService.
    Creates and provides a new AuthService instance bound to the current DB session.
    :param db: SQLAlchemy session provided by dependency injection.
    :return: AuthService instance.
    """
    repo = AuthRepository(db)
    return AuthService(repo)
