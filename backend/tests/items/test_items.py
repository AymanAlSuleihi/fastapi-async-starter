class TestItemsCRUD:
    async def test_list_items_empty(self, client):
        response = await client.get("/api/v1/items")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    async def test_create_item(self, client):
        response = await client.post(
            "/api/v1/items",
            json={"name": "Test Item", "description": "A test item", "price": 9.99},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Item"
        assert data["description"] == "A test item"
        assert data["price"] == 9.99
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data

    async def test_get_item(self, client):
        create_resp = await client.post(
            "/api/v1/items",
            json={"name": "Get Me", "price": 5.00},
        )
        item_id = create_resp.json()["id"]

        response = await client.get(f"/api/v1/items/{item_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Get Me"

    async def test_get_item_not_found(self, client):
        response = await client.get("/api/v1/items/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    async def test_update_item(self, client):
        create_resp = await client.post(
            "/api/v1/items",
            json={"name": "Original", "price": 10.00},
        )
        item_id = create_resp.json()["id"]

        response = await client.patch(
            f"/api/v1/items/{item_id}",
            json={"name": "Updated", "price": 20.00},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated"
        assert data["price"] == 20.00

    async def test_delete_item(self, client):
        create_resp = await client.post(
            "/api/v1/items",
            json={"name": "Delete Me"},
        )
        item_id = create_resp.json()["id"]

        response = await client.delete(f"/api/v1/items/{item_id}")
        assert response.status_code == 204

        # Verify deleted
        get_resp = await client.get(f"/api/v1/items/{item_id}")
        assert get_resp.status_code == 404

    async def test_list_items_pagination(self, client):
        for i in range(5):
            await client.post(
                "/api/v1/items",
                json={"name": f"Item {i}"},
            )

        response = await client.get("/api/v1/items?page=1&page_size=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5

    async def test_create_item_minimal(self, client):
        response = await client.post(
            "/api/v1/items",
            json={"name": "Minimal"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Minimal"
        assert data["description"] is None
        assert data["price"] is None
        assert data["is_active"] is True
