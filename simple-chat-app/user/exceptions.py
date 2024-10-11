from fastapi import HTTPException, status


class TokenExpiredException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")


class TokenNotFoundException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User already exist"
)
PasswordMismatchException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Passwords do not match"
)
InvalidEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
)
InvalidJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
)
UserIDNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="user ID not found"
)
ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="forbidden"
)
