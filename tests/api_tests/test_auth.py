from httpx import AsyncClient


async def test_get_me_unauthorized(ac: AsyncClient):
    """Тест получения профиля без авторизации (ожидается ошибка)."""
    response = await ac.get("/users/me")
    assert response.status_code in (401, 403)


async def test_add_user_success(ac: AsyncClient):
    """Тест успешного добавления пользователя."""
    payload = {
        "username": "testuser",
        "last_name": "Testov",
        "status": "HEAD",
        "password": "strongpassword123",
    }
    response = await ac.post("/users/", json=payload)

    assert response.status_code in (200, 201)
    data = response.json()
    assert data["username"] == payload["username"]
    assert "password" not in data  # Пароль не должен возвращаться в ответе


async def test_login_user_success(ac: AsyncClient, add_user_auth):
    """Тест успешного входа и установки Cookie."""
    payload = {
        "username": "test_user",
        "last_name": "test_last_name",
        "password": "test"
    }
    response = await ac.post("/users/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "access_token" in response.cookies


async def test_get_users(ac: AsyncClient):
    """Тест получения списка пользователей."""
    response = await ac.get("/users/")

    assert response.status_code == 200


async def test_get_me_authorized(ac: AsyncClient):
    """Тест получения своего профиля с переданным токеном/cookie."""
    # 1. Авторизуемся
    payload = {
        "username": "test_user",
        "last_name": "test_last_name",
        "password": "admin"
    }
    login_res = await ac.post("/users/login", json=payload)
    # token = login_res.json().get("access_token")

    # 2. Запрашиваем профиль (передавая Cookie или Authorization Header)
    # В зависимости от того, как AuthUserDep извлекает токен:
    # ac.cookies.set("access_token", token)
    response = await ac.get("/users/me")

    assert response.status_code == 200
    assert "user_id" in response.json()

# async def test_logout(self, ac: AsyncClient, test_get_me_authorized):
#     """Тест выхода из системы (удаление Cookie)."""
#     # Устанавливаем куку
#     ac.cookies.set("access_token", "fake_token")
#
#     response = await ac.post("/users/logout")
#
#     assert response.status_code == 200
#     assert response.json() == {"success": "Вы вышли из аккаунта"}
#     # Проверяем, что кука удалена или очищена
#     assert ac.cookies.get("access_token") is None