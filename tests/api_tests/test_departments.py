from httpx import AsyncClient
from src.schemas.departments import DepartmentCreateUpdateSchema


async def test_get_departments(ac: AsyncClient):
    res = await ac.get('/departments/')
    assert res.status_code == 200


async def test_403_post_dep(ac: AsyncClient, test_user):
    await test_user(title="test_user")
    payload = {
        "username": "test_user",
        "last_name": "test_user",
        "password": "test_user"
    }
    await ac.post("/users/login", json=payload)

    payload = DepartmentCreateUpdateSchema(title="test dep", description="test descript")
    res = await ac.post("/admin/departments/", json=payload.model_dump())
    assert res.status_code == 403


async def test_201_post_dep(admin_ac: AsyncClient):

    payload = DepartmentCreateUpdateSchema(title="test dep", description="test descript")
    res = await admin_ac.post("/admin/departments/", json=payload.model_dump())

    assert res.status_code == 200