from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    DB_HOST_TEST: str
    DB_PORT_TEST: str
    DB_NAME_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str

    REDIS_HOST: str
    REDIS_PORT: str

    SECRET: str


config = Config()
