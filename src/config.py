from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_URL: str
    SECRET: str


config = Config(_env_file=".env")
