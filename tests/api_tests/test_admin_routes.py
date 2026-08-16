import io
import uuid

import pytest

pytestmark = pytest.mark.asyncio


def unique_title(prefix: str = "task") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def make_upload_file(filename="file.txt", content=b"hello world"):
    return (filename, io.BytesIO(content), "text/plain")


class TestCreateTask:
    async def test_create_task_max(self, ac, test_department, test_user):
        department = await test_department(title="test_department")
        executor = await test_user(title="executor")
        title = unique_title()

        body = {
            "title": title,
            "description": "some description",
            "department_id": department.id,
            "executor_ids": [executor.id],  # было executors_ids — опечатка
        }

        response = await ac.post(
            "/tasks/",
            data=body,
            files={"attachments": make_upload_file()},
        )

        assert response.status_code == 200, response.text
        assert response.json()["title"] == title

    # async def test_create_task_missing_title_returns_422(self, ac):
    #     response = await ac.post("/tasks/", data={"description": "no title here"})
    #     assert response.status_code == 422
    #
    # async def test_create_task_with_nonexistent_executor_returns_error(self, ac):
    #     title = unique_title()
    #     response = await ac.post(
    #         "/tasks/",
    #         data={"title": title, "executor_ids": [999_999_999]},
    #     )
    #     assert response.status_code == 400
    #
    # async def test_create_task_with_attachment(self, ac):
    #     title = unique_title()
    #     response = await ac.post(
    #         "/tasks/",
    #         data={"title": title},
    #         files={"attachments": make_upload_file()},
    #     )
    #     assert response.status_code == 200, response.text
    #
    # async def test_create_task_duplicate_title_returns_error(self, ac):
    #     """title у Tasks unique=True — повторное создание с тем же title должно падать."""
    #     title = "Повторный заголовок"
    #     first = await ac.post("/tasks/", data={"title": title})
    #     assert first.status_code == 200, first.text
    #
    #     second = await ac.post("/tasks/", data={"title": title})
    #     assert second.status_code == 400
    #
    # async def test_create_task_with_department(self, ac, departments_create_1_2):
    #     title = unique_title()
    #     departments: list[int] = await departments_create_1_2()
    #
    #     response = await ac.post(
    #         "/tasks/",
    #         data={"title": title, "department_id": departments[1]},
    #     )
    #
    #     assert response.status_code == 200, response.text
    #     assert response.json()["department_id"] == departments[1]  # было захардкожено == 1


# ---------------------------------------------------------------------------
# GET /tasks/
# ---------------------------------------------------------------------------

# class TestGetTasks:
#     async def test_get_tasks_success(self, ac):
#         await ac.post("/tasks/", data={"title": unique_title()})
#         response = await ac.get("/tasks/", params={"limit": 10, "offset": 0})
#         assert response.status_code == 200, response.text
#
#     async def test_get_tasks_limit_out_of_range_returns_422(self, ac):
#         # QueryParamsSchema: limit = Field(10, gt=0, lt=20)
#         response = await ac.get("/tasks/", params={"limit": 50})
#         assert response.status_code == 422
#
#     async def test_get_tasks_negative_offset_returns_422(self, ac):
#         # offset = Field(0, ge=0)
#         response = await ac.get("/tasks/", params={"offset": -1})
#         assert response.status_code == 422


# ---------------------------------------------------------------------------
# PUT /tasks/{id}
# ---------------------------------------------------------------------------
# Секция была полностью закомментирована в исходнике — оставляю как есть,
# похоже на осознанный временный disable. Если она нужна, раскомментируйте
# и синтаксис/логика там валидны без изменений.
#
# class TestUpdateTask:
#     async def test_update_task_success(self, ac):
#         create_resp = await ac.post("/tasks/", data={"title": unique_title()})
#         task_id = create_resp.json()["id"]
#
#         new_title = unique_title("updated")
#         response = await ac.put(
#             f"/tasks/{task_id}",
#             data={"title": new_title, "description": "new description"},
#         )
#
#         assert response.status_code == 200, response.text
#         body = response.json()
#         assert body["title"] == new_title
#         assert body["description"] == "new description"
#
#     async def test_update_task_missing_title_returns_422(self, ac):
#         create_resp = await ac.post("/tasks/", data={"title": unique_title()})
#         task_id = create_resp.json()["id"]
#
#         response = await ac.put(f"/tasks/{task_id}", data={})
#         assert response.status_code == 422
#
#     async def test_update_task_invalid_id_type_returns_422(self, ac):
#         response = await ac.put("/tasks/not-an-int", data={"title": "x"})
#         assert response.status_code == 422
#
#     async def test_update_nonexistent_task_returns_error(self, ac):
#         response = await ac.put("/tasks/999999999", data={"title": unique_title()})
#         assert response.status_code != 200


# ---------------------------------------------------------------------------
# PATCH /tasks/{id}
# ---------------------------------------------------------------------------

# class TestUpdateExecutors:
#     async def test_patch_task_executors_success(self, ac, add_user):
#         create_resp = await ac.post("/tasks/", data={"title": unique_title()})
#         task_id = create_resp.json()["id"]
#
#         executor_1 = await add_user()
#
#         response = await ac.patch(
#             f"/tasks/{task_id}",
#             json={"executor_ids": [executor_1["id"]]},
#         )
#         assert response.status_code == 200, response.text
#
#     async def test_patch_task_missing_body_returns_422(self, ac):
#         create_resp = await ac.post("/tasks/", data={"title": unique_title()})
#         task_id = create_resp.json()["id"]
#
#         response = await ac.patch(f"/tasks/{task_id}", json={})
#         assert response.status_code == 422
#
#     async def test_patch_task_invalid_id_type_returns_422(self, ac):
#         response = await ac.patch("/tasks/not-an-int", json={"executor_ids": []})
#         assert response.status_code == 422
#
#     async def test_patch_task_returns_none_body(self, ac):
#         """
#         В текущей реализации ручка ничего явно не возвращает (return отсутствует,
#         стоит "pass" после комментария) — тело ответа будет null.
#         Если добавите return в ручке, этот тест нужно обновить.
#         """
#         create_resp = await ac.post("/tasks/", data={"title": unique_title()})
#         task_id = create_resp.json()["id"]
#
#         response = await ac.patch(f"/tasks/{task_id}", json={"executor_ids": []})
#
#         assert response.status_code == 200
#         assert response.json() is None


# ---------------------------------------------------------------------------
# POST /tasks/{id}/tasks_reply
# ---------------------------------------------------------------------------

# class TestCreateReply:
#     async def test_create_reply_success(self, ac):
#         create_resp = await ac.post("/tasks/", data={"title": unique_title()})
#         task_id = create_resp.json()["id"]
#
#         response = await ac.post(
#             f"/tasks/{task_id}/tasks_reply",
#             data={"content": "done"},
#         )
#         assert response.status_code == 200, response.text
#         assert response.json()["content"] == "done"
#
#     async def test_create_reply_missing_content_returns_422(self, ac):
#         create_resp = await ac.post("/tasks/", data={"title": unique_title()})
#         task_id = create_resp.json()["id"]
#
#         response = await ac.post(f"/tasks/{task_id}/tasks_reply", data={})
#         assert response.status_code == 422
#
#     async def test_create_reply_with_attachment(self, ac):
#         create_resp = await ac.post("/tasks/", data={"title": unique_title()})
#         task_id = create_resp.json()["id"]
#
#         response = await ac.post(
#             f"/tasks/{task_id}/tasks_reply",
#             data={"content": "with file"},
#             files={"attachments": make_upload_file()},
#         )
#         assert response.status_code == 200, response.text
#
#     async def test_create_reply_on_nonexistent_task_returns_error(self, ac):
#         response = await ac.post(
#             "/tasks/999999999/tasks_reply", data={"content": "irrelevant"}
#         )
#         assert response.status_code != 200


# ---------------------------------------------------------------------------
# DELETE /tasks/{id}
# ---------------------------------------------------------------------------

# class TestDeleteTask:
#     async def test_delete_own_task_success(self, ac):
#         create_resp = await ac.post("/tasks/", data={"title": unique_title()})
#         task_id = create_resp.json()["id"]
#
#         response = await ac.delete(f"/tasks/{task_id}")
#
#         # ВНИМАНИЕ: в роутере `return 200, {'status': 'delete success'}` — это
#         # tuple, а не Response/dict. FastAPI сериализует его как JSON-массив
#         # [200, {...}], HTTP-статус при этом остаётся 200 (дефолтный), а не тот,
#         # что передавали руками. Стоит поправить на `return {'status': ...}`.
#         assert response.status_code == 200
#         assert response.json() == [200, {"status": "delete success"}]
#
#     async def test_delete_task_invalid_id_returns_422(self, ac):
#         response = await ac.delete("/tasks/abc")
#         assert response.status_code == 422
#
#     async def test_delete_nonexistent_task_returns_error(self, ac):
#         response = await ac.delete("/tasks/999999999")
#         assert response.status_code != 200
#
#     async def test_delete_other_users_task_forbidden(self, ac, admin_ac):
#         """Комментарий в роутере: "удалить только свою задачу".
#         Создаём задачу от имени admin_ac и пробуем удалить её через ac (test_user) —
#         ожидаем отказ. Конкретный код зависит от реализации delete_task в сервисе,
#         сейчас проверяем только что это не 200 — уточните под реальный код (403/404)."""
#         create_resp = await admin_ac.post("/tasks/", data={"title": unique_title()})
#         task_id = create_resp.json()["id"]
#
#         response = await ac.delete(f"/tasks/{task_id}")
#         assert response.status_code != 200