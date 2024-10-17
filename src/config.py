import sys

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_URL: str
    TEST_DB_URL: str
    SECRET: str


config = Config(_env_file="./../.env" if "uvicorn" in sys.argv[0] else "./.env")
