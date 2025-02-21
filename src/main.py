import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis
from fastapi.staticfiles import StaticFiles

from auth.auth import auth_backend, fastapi_users, current_user
from config import config
from models import User
from auth.schemas import UserRead, UserCreate
from companies.router import router as router_authors
from assets.router import router as router_books
from transactions.router import router as router_borrowings
from pages.router import router as router_pages
from balance.router import router as router_balance


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="Library app", lifespan=lifespan)

app.mount(
    "/static",
    StaticFiles(directory="static" if "uvicorn" in sys.argv[0] or "gunicorn" in sys.argv[0] else "src/static"),
    name="static",
)


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.get("/user", tags=["User"])
def get_current_user(user: User = Depends(current_user)):
    return UserRead(
        id=user.id,
        email=user.email,
        username=user.username,
        balance=user.balance,
        role_id=user.role_id,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        is_verified=user.is_verified,
    )


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

app.include_router(router_authors)
app.include_router(router_books)
app.include_router(router_borrowings)
app.include_router(router_pages)
app.include_router(router_balance)
