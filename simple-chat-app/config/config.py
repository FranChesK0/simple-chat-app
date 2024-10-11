import os
from typing import NamedTuple

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env"
        )
    )

    SECRET_KEY: str = "xxx"
    ALGORITHM: str = "HS256"


class AuthData(NamedTuple):
    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()


def get_auth_data() -> AuthData:
    return AuthData(settings.SECRET_KEY, settings.ALGORITHM)
