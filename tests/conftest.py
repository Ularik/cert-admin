from src.schemas.users import UserOutSchema
from src.database import engine_null_pool, Base
from src.main import app
from src.config import settings
from src.models import *  # импортируем все таблицы для Base metadata
import pytest
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator
from src.schemas.departments import DepartmentsOutSchema

# session, “function”, “class”, “module”, “package”,
@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function", autouse=True)
async def setup_database(check_mode):  # очередность выполнения
    print("-------Fixtures start-----------")
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function", autouse=False)
async def test_user(setup_database, ac):
    async def wrapper(title: str = "test_user") -> UserOutSchema:
        response = await ac.post(
            "/users/",
            json={
                "username": title,
                "last_name": title,
                "password": title
            }
        )
        user = response.json()
        assert user['username']
        return user

    return wrapper

@pytest.fixture(scope="function", autouse=False)
async def test_department(setup_database, admin_ac):
    async def wrapper(title: str = "test_department"):
        response = await admin_ac.post(
            "/admin/departments/",
            json={
                "title": title,
                "description": title,
            }
        )
        department = response.json()
        return department

    return wrapper

@pytest.fixture(scope="function", autouse=False)
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
    user = response.json()
    assert user['username']
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