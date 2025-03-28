import os
from pathlib import Path

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: str

    SECRET: str
    DEBUG: bool

    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_FROM: str | None = None
    MAIL_PORT: int | None = None
    MAIL_SERVER: str | None = None
    MAIL_FROM_NAME: str | None = None
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    model_config = ConfigDict(
        env_file=Path("") if os.getenv("DOCKER_ENV", "").lower() == "true" else ".env.dev", env_file_encoding="utf-8"
    )


config = Config()
