from fastapi import FastAPI

from src.auth.auth import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.authors.router import router as router_books

app = FastAPI(title="Library app")


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_books)
