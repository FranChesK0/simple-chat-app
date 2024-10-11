from typing import Dict, List, Optional

from fastapi import Response, APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .dao import UserDAO
from .auth import authenticate_user, get_password_hash, create_access_token
from .models import User
from .schemas import UserAuth, UserRead, UserRegister
from .exceptions import (
    PasswordMismatchException,
    UserAlreadyExistsException,
    InvalidEmailOrPasswordException,
)

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="simple-chat-app/templates")


@router.get("/users", response_model=List[UserRead])
async def get_users() -> List:
    users: List[User] = await UserDAO.find_all()
    return list(map(lambda u: {"id": u.id, "name": u.name}, users))


@router.get("/", response_class=HTMLResponse, summary="Authorization Page")
async def get_categories(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("auth.html", {"request": request})


@router.post("/register/")
async def register_user(user_data: UserRegister) -> Dict:
    user: Optional[User] = await UserDAO.find_by(email=user_data.email)
    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:
        raise PasswordMismatchException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(
        name=user_data.name, email=user_data.email, hashed_password=hashed_password
    )
    return {"message": "Registration successful"}


@router.post("/login/")
async def auth_user(response: Response, user_data: UserAuth) -> Dict:
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise InvalidEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {
        "ok": True,
        "access_token": access_token,
        "refresh_token": None,
        "message": "Authorization successful",
    }


@router.post("/logout/")
async def logout_user(response: Response) -> Dict:
    response.delete_cookie(key="users_access_token")
    return {"message": "User exited"}
