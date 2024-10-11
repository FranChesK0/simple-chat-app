from typing import Optional
from datetime import datetime, timezone

from jose import JWTError, jwt
from fastapi import Depends, Request, HTTPException, status

from config import get_auth_data

from .dao import UserDAO
from .models import User
from .exceptions import (
    InvalidJwtException,
    TokenExpiredException,
    TokenNotFoundException,
    UserIDNotFoundException,
)


def get_token(request: Request) -> str:
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNotFoundException
    return token


async def get_current_user(token: str = Depends(get_token)) -> User:
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data.SECRET_KEY, auth_data.ALGORITHM)
    except JWTError:
        raise InvalidJwtException

    expire = str(payload.get("exp"))
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if not expire or expire_time < datetime.now(timezone.utc):
        raise TokenExpiredException

    user_id = str(payload.get("sub"))
    if not user_id:
        raise UserIDNotFoundException

    user: Optional[User] = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
