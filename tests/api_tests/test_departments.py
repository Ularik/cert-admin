from httpx import AsyncClient
from src.schemas.departments import DepartmentCreateSchema


async def test_get_departments(ac: AsyncClient):
    res = await ac.get('/departments/')
    assert res.status_code == 200


async def test_403_post_dep(ac: AsyncClient):

    payload = DepartmentCreateSchema(title="test dep", description="test descript")
    res = await ac.post("/admin/departments/", json=payload.model_json_schema())

    assert res.status_code == 403


async def test_201_post_dep(admin_ac: AsyncClient):

    payload = DepartmentCreateSchema(title="test dep", description="test descript")
    res = await admin_ac.post("/admin/departments/", json=payload.model_json_schema())

    assert res.status_code == 200