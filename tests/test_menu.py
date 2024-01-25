from fastapi.testclient import TestClient

from core import app

client = TestClient(app)


class Test_Menu:
    id = ""

    @classmethod
    def test_create_items(cls):
        data = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = client.post("/api/v1/menus", json=data)
        response_data = response.json()
        cls.id = response_data["id"]
        assert response.status_code == 201
        assert "id" in response_data
        assert response_data["title"] == data["title"]
        assert response_data["description"] == data["description"]

    @classmethod
    def test_read_menu(cls):
        response = client.get(f"/api/v1/menus/{cls.id}")
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        assert response_data["title"] == "My menu 1"
        assert response_data["description"] == "My menu description 1"

    @classmethod
    def test_read_menus(cls):
        response = client.get("/api/v1/menus")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "My menu 1"
        assert data[0]["description"] == "My menu description 1"

    @classmethod
    def test_update_menu(cls):
        updated_data = {
            "title": "My updated menu 1",
            "description": "My updated menu description 1"
        }
        response = client.patch(f"/api/v1/menus/{cls.id}", json=updated_data)
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        assert response_data["title"] == updated_data["title"]
        assert response_data["description"] == updated_data["description"]

    @classmethod
    def test_delete_menu(cls):
        response = client.delete(f"/api/v1/menus/{cls.id}")
        assert response.status_code == 200
        assert not response.json()
