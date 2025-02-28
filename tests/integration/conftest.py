import os
from typing import AsyncGenerator, Annotated, TypeVar, get_args, Callable, Awaitable

import pytest
from dotenv import load_dotenv
from fastapi import Depends, params
from httpx import AsyncClient, ASGITransport
from pytest_asyncio import is_async_test
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from auth.auth import current_user_admin, current_user
from models import User
from database import get_async_session, Base
from main import app

load_dotenv(".env.test", override=True)

url = (
    f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine_test = create_async_engine(url)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
metadata = Base.metadata
metadata.bind = engine_test


T = TypeVar("T")


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


def get_fastapi_dependency_from_annotation(a: Annotated[T, params.Depends]) -> T:
    return get_args(a)[1].dependency


AdminUser = Annotated[User, Depends(current_user_admin)]
CurrentUser = Annotated[User, Depends(current_user)]


@pytest.fixture(scope="session")
def get_admin_client():
    async def _authenticated_client(user: User) -> AsyncClient:
        # Override the dependency to act as if a user is authenticated

        dep = get_fastapi_dependency_from_annotation(AdminUser)
        app.dependency_overrides[dep] = lambda: user

        dep = get_fastapi_dependency_from_annotation(CurrentUser)
        app.dependency_overrides[dep] = lambda: user

        return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")

    yield _authenticated_client

    app.dependency_overrides = {}


GetAdminClient = Callable[[User], Awaitable[AsyncClient]]


@pytest.fixture(scope="session")
async def session_fixture() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def admin_client(get_admin_client: GetAdminClient, session_fixture):
    user = User(
        username="admin", email="admin@test.com", hashed_password="test", role_id=2, is_superuser=True, balance=1000.0
    )
    async with session_fixture as session:
        session.add(user)
        await session.commit()

    client = await get_admin_client(user)
    return client


def pytest_collection_modifyitems(session, items):
    order = {
        "tests/integration/test_auth.py": 0,
        "tests/integration/test_companies.py": 1,
        "tests/integration/test_assets.py": 2,
        "tests/integration/test_transactions.py": 3,
    }

    root_path = str(session.config.rootpath)
    items.sort(key=lambda item: order.get(str(item.fspath.relto(root_path)), 99))

    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(loop_scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)
