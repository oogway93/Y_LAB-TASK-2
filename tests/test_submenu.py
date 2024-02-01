from fastapi.testclient import TestClient

from core import app
from tests.utils import url_for

client = TestClient(app)


class TestSubmenu:
    """Test Class Submenu"""
    menu_id: str = ''
    id: str = ''

    @classmethod
    def test_create_menu(cls):
        data = {
            'title': 'My menu 1',
            'description': 'My menu description 1'
        }
        response = client.post(url_for('create_menu'), json=data)
        assert response.status_code == 201
        response_data = response.json()
        cls.menu_id = response_data['id']
        assert 'id' in response_data
        assert response_data['title'] == data['title']
        assert response_data['description'] == data['description']

    @classmethod
    def test_create_submenu(cls):
        data = {
            'title': 'My submenu 1',
            'description': 'My submenu description 1'
        }
        response = client.post(url_for('create_submenu', menu_id=cls.menu_id), json=data)
        assert response.status_code == 201
        response_data = response.json()
        cls.id = response_data['id']
        assert 'id' in response_data
        assert response_data['title'] == data['title']
        assert response_data['description'] == data['description']

    @classmethod
    def test_read_submenu(cls):
        response = client.get(url_for('get_submenu', menu_id=cls.menu_id, id=cls.id))
        assert response.status_code == 200
        response_data = response.json()
        assert 'id' in response_data
        assert response_data['title'] == 'My submenu 1'
        assert response_data['description'] == 'My submenu description 1'

    @classmethod
    def test_read_submenus(cls):
        response = client.get(url_for('get_all_submenus', menu_id=cls.menu_id))
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 1
        assert response_data[0]['title'] == 'My submenu 1'
        assert response_data[0]['description'] == 'My submenu description 1'

    @classmethod
    def test_update_submenu(cls):
        updated_data = {
            'title': 'My updated submenu 1',
            'description': 'My updated submenu description 1'
        }
        response = client.patch(url_for('update_submenu', menu_id=cls.menu_id, id=cls.id), json=updated_data)
        assert response.status_code == 200
        response_data = response.json()
        assert 'id' in response_data
        assert response_data['title'] == updated_data['title']
        assert response_data['description'] == updated_data['description']

    @classmethod
    def test_delete_submenu(cls):
        response = client.delete(url_for('delete_submenu', menu_id=cls.menu_id, id=cls.id))
        assert response.status_code == 200
        assert not response.json()

    @classmethod
    def test_delete_menu(cls):
        response = client.delete(url_for('delete_menu', id=cls.menu_id))
        assert response.status_code == 200
        assert not response.json()
