from fastapi.testclient import TestClient

from core import app

client = TestClient(app)


class Test_Submenu:
    menu_id = ""
    id = ""

    @classmethod
    def test_create_menu(cls):
        data = {
            "title": "My menu 1",
            "description": "My menu description 1"
        }
        response = client.post("/api/v1/menus", json=data)
        assert response.status_code == 201
        response_data = response.json()
        cls.menu_id = response_data["id"]
        assert "id" in response_data
        assert response_data["title"] == data["title"]
        assert response_data["description"] == data["description"]

    @classmethod
    def test_create_submenu(cls):
        data = {
            "title": "My submenu 1",
            "description": "My submenu description 1"
        }
        response = client.post(f"/api/v1/menus/{cls.menu_id}/submenus", json=data)
        assert response.status_code == 201
        response_data = response.json()
        cls.id = response_data["id"]
        assert "id" in response_data
        assert response_data["title"] == data["title"]
        assert response_data["description"] == data["description"]

    @classmethod
    def test_read_submenu(cls):
        response = client.get(f"/api/v1/menus/{cls.menu_id}/submenus/{cls.id}")
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        assert response_data["title"] == "My submenu 1"
        assert response_data["description"] == "My submenu description 1"

    @classmethod
    def test_read_submenus(cls):
        response = client.get(f"/api/v1/menus/{cls.menu_id}/submenus")
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 1
        assert response_data[0]["title"] == "My submenu 1"
        assert response_data[0]["description"] == "My submenu description 1"

    @classmethod
    def test_update_menu(cls):
        updated_data = {
            "title": "My updated submenu 1",
            "description": "My updated submenu description 1"
        }
        response = client.patch(f"/api/v1/menus/{cls.menu_id}/submenus/{cls.id}", json=updated_data)
        assert response.status_code == 200
        response_data = response.json()
        assert "id" in response_data
        assert response_data["title"] == updated_data["title"]
        assert response_data["description"] == updated_data["description"]

    @classmethod
    def test_delete_submenu(cls):
        response = client.delete(f"/api/v1/menus/{cls.menu_id}/submenus/{cls.id}")
        assert response.status_code == 200
        assert not response.json()

    @classmethod
    def test_delete_menu(cls):
        response = client.delete(f"/api/v1/menus/{cls.menu_id}")
        assert response.status_code == 200
        assert not response.json()
