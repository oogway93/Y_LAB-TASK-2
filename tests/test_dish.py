from fastapi.testclient import TestClient

from core import app

client = TestClient(app)

menu_id = ""


class Test_Dish:
    menu_id = ""
    submenu_id = ""
    id = ""

    @classmethod
    def test_create_menu(cls):
        data = {"title": "My menu 1", "description": "My menu description 1"}
        response = client.post("/api/v1/menus", json=data)
        response_data = response.json()
        cls.menu_id = response_data["id"]
        assert response.status_code == 201
        assert "id" in response_data
        assert response_data["title"] == data["title"]
        assert response_data["description"] == data["description"]

    @classmethod
    def test_create_submenu(cls):
        data = {"title": "My submenu 1", "description": "My submenu description 1"}
        response = client.post(f"/api/v1/menus/{cls.menu_id}/submenus", json=data)
        response_data = response.json()
        cls.submenu_id = response_data["id"]
        assert response.status_code == 201
        assert "id" in response_data
        assert response_data["title"] == data["title"]
        assert response_data["description"] == data["description"]

    @classmethod
    def test_create_dish(cls):
        data = {"title": "My dish 1", "description": "My dish description 1", "price": "12.50"}
        response = client.post(f"/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes", json=data)
        response_data = response.json()
        cls.id = response_data["id"]
        assert response.status_code == 201
        assert "id" in response_data
        assert response_data["title"] == data["title"]
        assert response_data["description"] == data["description"]
        assert response_data["price"] == data["price"][:-1]

    @classmethod
    def test_read_dish(cls):
        response = client.get(f"/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes/{cls.id}")
        assert response.status_code == 200

    @classmethod
    def test_read_dishes(cls):
        response = client.get(f"/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "My dish 1"
        assert data[0]["description"] == "My dish description 1"
        assert data[0]["price"] == 12.5

    @classmethod
    def test_update_dish(cls):
        updated_data = {
            "title": "My updated dish 1",
            "description": "My updated dish description 1",
            "price": "14.50"
        }
        response = client.patch(f"/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes/{cls.id}",
                                json=updated_data)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["title"] == updated_data["title"]
        assert response_data["description"] == updated_data["description"]
        assert response_data["price"] == updated_data["price"][:-1]

    @classmethod
    def test_delete_dish(cls):
        response = client.delete(f"/api/v1/menus/{cls.menu_id}/submenus/{cls.submenu_id}/dishes/{cls.id}")
        assert response.status_code == 200
        assert not response.json()

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
