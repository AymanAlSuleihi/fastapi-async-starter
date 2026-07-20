class TestUserAuth:
    async def test_login_success(self, client, admin_token):
        assert admin_token is not None
        assert len(admin_token) > 0

    async def test_login_invalid_credentials(self, client):
        response = await client.post(
            "/api/v1/users/login",
            json={"email": "wrong@example.com", "password": "wrongpass"},
        )
        assert response.status_code == 400
        data = response.json()
        assert data["code"] == "INVALID_CREDENTIALS"

    async def test_get_me(self, client, admin_headers):
        response = await client.get("/api/v1/users/me", headers=admin_headers)
        assert response.status_code == 200
        assert response.json()["email"] == "admin@example.com"

    async def test_update_me(self, client, admin_headers):
        response = await client.patch(
            "/api/v1/users/me",
            headers=admin_headers,
            json={"first_name": "Updated"},
        )
        assert response.status_code == 200
        assert response.json()["first_name"] == "Updated"

    async def test_list_users_requires_auth(self, client):
        response = await client.get("/api/v1/users")
        assert response.status_code == 403


class TestUserCRUD:
    async def test_list_users(self, client, admin_headers):
        response = await client.get("/api/v1/users", headers=admin_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_create_user(self, client, admin_headers):
        response = await client.post(
            "/api/v1/users",
            headers=admin_headers,
            json={
                "email": "test@example.com",
                "password": "testpass123",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert "id" in data

    async def test_create_user_requires_admin(self, client, admin_headers):
        # Create a non-admin user first
        await client.post(
            "/api/v1/users",
            headers=admin_headers,
            json={
                "email": "regular@example.com",
                "password": "testpass123",
                "first_name": "Regular",
                "last_name": "User",
                "is_admin": False,
            },
        )
        # Login as regular user
        login_resp = await client.post(
            "/api/v1/users/login",
            json={"email": "regular@example.com", "password": "testpass123"},
        )
        regular_headers = {"Authorization": f"Bearer {login_resp.json()['access_token']}"}

        # Regular user cannot create users
        response = await client.post(
            "/api/v1/users",
            headers=regular_headers,
            json={
                "email": "nope@example.com",
                "password": "testpass123",
                "first_name": "Nope",
                "last_name": "User",
            },
        )
        assert response.status_code == 403

    async def test_create_user_duplicate_email(self, client, admin_headers):
        await client.post(
            "/api/v1/users",
            headers=admin_headers,
            json={
                "email": "dup@example.com",
                "password": "testpass123",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        response = await client.post(
            "/api/v1/users",
            headers=admin_headers,
            json={
                "email": "dup@example.com",
                "password": "testpass123",
                "first_name": "Test",
                "last_name": "User",
            },
        )
        assert response.status_code == 409
        assert response.json()["code"] == "USER_ALREADY_EXISTS"

    async def test_update_user(self, client, admin_headers):
        create_resp = await client.post(
            "/api/v1/users",
            headers=admin_headers,
            json={
                "email": "update@example.com",
                "password": "testpass123",
                "first_name": "Old",
                "last_name": "Name",
            },
        )
        user_id = create_resp.json()["id"]
        response = await client.patch(
            f"/api/v1/users/{user_id}",
            headers=admin_headers,
            json={"first_name": "New", "last_name": "NewLast"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "New"
        assert data["last_name"] == "NewLast"

    async def test_update_user_not_found(self, client, admin_headers):
        response = await client.patch(
            "/api/v1/users/00000000-0000-0000-0000-000000000000",
            headers=admin_headers,
            json={"first_name": "Ghost"},
        )
        assert response.status_code == 404

    async def test_update_user_email_and_password(self, client, admin_headers):
        create_resp = await client.post(
            "/api/v1/users",
            headers=admin_headers,
            json={
                "email": "multi@example.com",
                "password": "testpass123",
                "first_name": "Multi",
                "last_name": "Field",
            },
        )
        user_id = create_resp.json()["id"]
        response = await client.patch(
            f"/api/v1/users/{user_id}",
            headers=admin_headers,
            json={
                "email": "changed@example.com",
                "password": "newpass456",
                "is_admin": True,
                "is_active": False,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "changed@example.com"
        assert data["is_admin"] is True
        assert data["is_active"] is False

    async def test_delete_user(self, client, admin_headers):
        create_resp = await client.post(
            "/api/v1/users",
            headers=admin_headers,
            json={
                "email": "delete@example.com",
                "password": "testpass123",
                "first_name": "Delete",
                "last_name": "Me",
            },
        )
        user_id = create_resp.json()["id"]
        response = await client.delete(f"/api/v1/users/{user_id}", headers=admin_headers)
        assert response.status_code == 204
        list_resp = await client.get("/api/v1/users", headers=admin_headers)
        emails = [u["email"] for u in list_resp.json()]
        assert "delete@example.com" not in emails

    async def test_delete_user_not_found(self, client, admin_headers):
        response = await client.delete(
            "/api/v1/users/00000000-0000-0000-0000-000000000000",
            headers=admin_headers,
        )
        assert response.status_code == 404

    async def test_auth_invalid_token(self, client):
        response = await client.get(
            "/api/v1/users",
            headers={"Authorization": "Bearer invalid.token.here"},
        )
        assert response.status_code == 400
        assert response.json()["code"] == "INVALID_CREDENTIALS"

    async def test_auth_token_without_sub(self, client):
        """A valid JWT without a 'sub' claim is rejected with 403."""
        from src.auth.utils import create_access_token

        token = create_access_token({"other": "data"})  # no 'sub' claim
        response = await client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    async def test_inactive_user_forbidden(self, client, admin_headers):
        """An inactive user can login but cannot access protected endpoints."""
        # Admin creates an inactive user
        await client.post(
            "/api/v1/users",
            headers=admin_headers,
            json={
                "email": "inactive@example.com",
                "password": "testpass123",
                "first_name": "Inactive",
                "last_name": "User",
                "is_active": False,
            },
        )
        # Login as the inactive user (login does not check is_active)
        login_resp = await client.post(
            "/api/v1/users/login",
            json={"email": "inactive@example.com", "password": "testpass123"},
        )
        assert login_resp.status_code == 200
        inactive_headers = {"Authorization": f"Bearer {login_resp.json()['access_token']}"}

        # Accessing /me with an inactive user is forbidden
        response = await client.get("/api/v1/users/me", headers=inactive_headers)
        assert response.status_code == 403


class TestErrorHandlers:
    async def test_unhandled_exception_returns_500(self):
        """A plain Exception (not AppException) triggers the unhandled handler → 500."""
        from fastapi import FastAPI
        from starlette.testclient import TestClient

        from src.extensions.error_handlers import register_error_handlers

        app = FastAPI()
        register_error_handlers(app)

        @app.get("/boom")
        async def boom():
            raise Exception("unexpected error")

        # TestClient handles ServerErrorMiddleware's re-raised exception properly
        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.get("/boom")
            assert response.status_code == 500
            data = response.json()
            assert data["detail"] == "Internal server error"
            assert "code" not in data


class TestHealth:
    async def test_health_check(self, client):
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
