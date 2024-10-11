from typing import Dict, Optional
from datetime import datetime, timezone, timedelta

from jose import jwt
from pydantic import EmailStr
from passlib.context import CryptContext

from config import get_auth_data

from .dao import UserDAO
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=360)
    to_encode.update({"exp": expire})
    auth_data = get_auth_data()
    encoded_jwt = jwt.encode(to_encode, auth_data.SECRET_KEY, auth_data.ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str) -> Optional[User]:
    user: Optional[User] = await UserDAO.find_by(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
