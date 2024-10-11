from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from chat import router as chat_router
from user import TokenExpiredException, TokenNotFoundException
from user import router as user_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="simple-chat-app/static"), name="static")

CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(chat_router)


@app.get("/")
async def redirect_to_auth() -> RedirectResponse:
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(
    request: Request, exc: HTTPException
) -> RedirectResponse:
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenNotFoundException)
async def token_not_found_exception_handler(
    request: Request, exc: HTTPException
) -> RedirectResponse:
    return RedirectResponse(url="/auth")
