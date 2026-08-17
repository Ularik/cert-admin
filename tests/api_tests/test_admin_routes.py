import io
import uuid
from docx import Document

def make_real_docx_file(filename="task1.docx", text="Test document content"):
    doc = Document()
    doc.add_paragraph(text)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return (
        filename,
        buffer,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


def unique_title(prefix: str = "task") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def make_upload_file(filename="file.txt", content=b"hello world"):
    return (filename, io.BytesIO(content), "text/plain")


class TestCreateTask:
    async def test_create_task_max(self, admin_ac, test_department, test_user):
        department = await test_department(title="test_department")
        executor = await test_user(title="executor")
        title = unique_title()

        body = {
            "title": title,
            "description": "some description",
            "department_id": department['id'],
            "executor_ids": [executor['id']],
        }

        files = [
            ("attachments", make_upload_file("report.pdf", b"pdf content")),
            ("attachments", make_real_docx_file("report.docx")),
        ]

        response = await admin_ac.post(
            "/admin/tasks/",
            data=body,
            files=files,
        )

        assert response.status_code == 200
        res = response.json()
        assert len(res["attachments"]) == 2


    async def test_create_task_missing_title_returns_422(self, admin_ac):
        response = await admin_ac.post("/admin/tasks/", data={"description": "no title here"})
        assert response.status_code == 422

    async def test_create_task_with_nonexistent_executor_returns_error(self, admin_ac):
        title = unique_title()
        response = await admin_ac.post(
            "/admin/tasks/",
            data={"title": title, "executor_ids": [999_999_999]},
        )
        assert response.status_code == 400

    async def test_create_task_with_duplicate_attachment(self, admin_ac):
        title = unique_title()
        files = [
            ("attachments", make_real_docx_file("report.docx")),
            ("attachments", make_real_docx_file("report.docx")),
            ("attachments", make_real_docx_file("report.docx")),
        ]
        response = await admin_ac.post(
            "/admin/tasks/",
            data={"title": title},
            files=files,
        )
        assert response.status_code == 200
        res = response.json()
        print(res['attachments'])
        assert len(res['attachments']) == 1

    async def test_create_task_duplicate_title_returns_error(self, admin_ac):
        """title у Tasks unique=True — повторное создание с тем же title должно падать."""
        title = "Повторный заголовок"
        first = await admin_ac.post("/admin/tasks/", data={"title": title})
        assert first.status_code == 200, first.text

        second = await admin_ac.post("/admin/tasks/", data={"title": title})
        assert second.status_code == 400


# ---------------------------------------------------------------------------
# GET /tasks/
# ---------------------------------------------------------------------------

class TestGetTasks:
    async def test_get_tasks_success(self, admin_ac):
        await admin_ac.post("/admin/tasks/", data={"title": unique_title()})
        response = await admin_ac.get("/admin/tasks/", params={"limit": 10, "offset": 0})
        assert response.status_code == 200

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

class TestUpdateTask:
    async def test_update_task(self, admin_ac):
        create_resp = await admin_ac.post("/admin/tasks/",
                                          data={"title": unique_title()},
                                          files=[
                                              ("attachments", make_real_docx_file("test.docx")),
                                              ("attachments", make_real_docx_file("test2.docx")),
                                          ]
                                          )
        response = create_resp.json()
        assert create_resp.status_code == 200
        task_id = response["id"]
        old_attachment = response['attachments'][0]

        new_title = unique_title("updated")
        response = await admin_ac.put(
            f"/admin/tasks/{task_id}",
            data={
                "title": new_title,
                "old_attachments_datas": [old_attachment['id']]
            },
            files=[
                ("attachments", make_real_docx_file("new_test.docx")),
                ("attachments", make_real_docx_file(old_attachment['filename'])), # check on duplicate
            ]
        )

        assert response.status_code == 200
        body = response.json()
        assert body["title"] == new_title
        print(body["attachments"])
        assert len(body["attachments"]) == 2
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

class TestUpdateExecutors:
    async def test_patch_task_executors_success(self, admin_ac, test_user):
        create_resp = await admin_ac.post("/admin/tasks/", data={"title": unique_title()})
        task_id = create_resp.json()["id"]

        executor_1 = await test_user(title='test')

        response = await admin_ac.patch(
            f"/admin/tasks/{task_id}",
            json={"executor_ids": [executor_1["id"]]},
        )
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# POST /tasks/{id}/tasks_reply
# ---------------------------------------------------------------------------

class TestCreateReply:
    async def test_create_reply_success(self, admin_ac):
        create_resp = await admin_ac.post("/admin/tasks/", data={"title": unique_title()})

        assert create_resp.status_code == 200
        task_id = create_resp.json()["id"]

        files = [
            ('attachments', make_real_docx_file('response.docx'))
        ]

        response = await admin_ac.post(
            f"/admin/tasks/{task_id}/tasks_reply",
            data={"content": "done"},
            files=files
        )
        assert response.status_code == 200
        assert response.json()["content"] == "done"

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