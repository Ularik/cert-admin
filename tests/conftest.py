from src.database import engine_null_pool, Base
from src.main import app
from src.config import settings
from src.models import *  # импортируем все таблицы для Base metadata
import pytest
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator


# session, “function”, “class”, “module”, “package”,
@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_mode):  # очередность выполнения
    print("-------Fixtures start-----------")
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def add_user_auth(setup_database, ac):
    response = await ac.post(
        "/users/",
        json={
            "username": "test_user",
            "last_name": "test_last_name",
            "password": "test"
        }
    )
    user = response.json()
    assert user['username']
    return user


@pytest.fixture(scope="session")
async def admin_ac(ac) -> AsyncGenerator[AsyncClient]:
    response = await ac.post(
        "/users/",
        json={
            "username": "admin",
            "last_name": "admin",
            "status": "ADMIN",
            "password": "admin"
        }
    )

    assert response.status_code == 200

    await ac.post(
        "/users/login",
        json={
            "username": "admin",
            "last_name": "admin",
            "password": "admin"
        }
    )
    assert ac.cookies['access_token']
    yield ac