from pydantic import Field, EmailStr, BaseModel


class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(
        ..., min_length=4, max_length=50, description="Password (4-50 symbols)"
    )
    password_check: str = Field(
        ..., min_length=4, max_length=50, description="Password (4-50 symbols)"
    )
    name: str = Field(..., min_length=3, max_length=50, description="Name (3-50 symbols)")


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(
        ..., min_length=4, max_length=50, description="Password (4-50 symbols)"
    )


class UserRead(BaseModel):
    id: int = Field(..., description="User ID")
    name: str = Field(..., min_length=3, max_length=50, description="Name (3-50 symbols)")
