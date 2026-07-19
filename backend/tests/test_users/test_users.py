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
            json={"first_name": "New"},
        )
        assert response.status_code == 200
        assert response.json()["first_name"] == "New"

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
            json={"email": "changed@example.com", "password": "newpass456", "is_active": False},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "changed@example.com"
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
