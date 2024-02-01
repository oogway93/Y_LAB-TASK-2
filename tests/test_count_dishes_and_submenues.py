from fastapi.testclient import TestClient

from core import app
from tests.utils import reverse

client = TestClient(app)


class TestCounting:
    """Test Class Counting dishes and submenus"""
    menu_id: str = ''
    submenu_id: str = ''

    @classmethod
    def test_create_menu(cls):
        data = {'title': 'My menu 1', 'description': 'My menu description 1'}
        response = client.post(reverse('create_menu'), json=data)
        response_data = response.json()
        cls.menu_id = response_data['id']
        assert response.status_code == 201
        assert 'id' in response_data
        assert response_data['title'] == data['title']
        assert response_data['description'] == data['description']

    @classmethod
    def test_create_submenu(cls):
        data = {'title': 'My submenu 1', 'description': 'My submenu description 1'}
        response = client.post(reverse('create_submenu', menu_id=cls.menu_id), json=data)
        response_data = response.json()
        cls.submenu_id = response_data['id']
        assert response.status_code == 201
        assert 'id' in response_data
        assert response_data['title'] == data['title']
        assert response_data['description'] == data['description']

    @classmethod
    def test_create_dish(cls):
        data = {
            'title': 'My dish 2',
            'description': 'My dish description 2',
            'price': '13.50'
        }
        data2 = {
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50'
        }
        response = client.post(reverse('create_dish', menu_id=cls.menu_id, submenu_id=cls.submenu_id), json=data)
        response2 = client.post(reverse('create_dish', menu_id=cls.menu_id, submenu_id=cls.submenu_id), json=data2)
        response_data = response.json()
        response_data2 = response2.json()
        assert response.status_code == 201
        assert response2.status_code == 201
        assert 'id' in response_data
        assert 'id' in response_data2
        assert response_data['title'] == data['title']
        assert response_data['description'] == data['description']
        assert response_data['price'] == data['price'][:-1]
        assert response_data2['title'] == data2['title']
        assert response_data2['description'] == data2['description']
        assert response_data2['price'] == data2['price'][:-1]

    @classmethod
    def test_read_menu(cls):
        response = client.get(reverse('get_menu', id=cls.menu_id))
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data
        assert data['submenus_count'] == 1
        assert data['dishes_count'] == 2

    @classmethod
    def test_read_submenu(cls):
        response = client.get(reverse('get_submenu', menu_id=cls.menu_id, id=cls.submenu_id))
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data
        assert data['dishes_count'] == 2

    @classmethod
    def test_delete_submenu(cls):
        response = client.delete(reverse('delete_submenu', menu_id=cls.menu_id, id=cls.submenu_id))
        assert response.status_code == 200
        assert not response.json()

    @classmethod
    def test_read_submenus_after_delete(cls):
        response = client.get(reverse('get_all_submenus', menu_id=cls.menu_id))
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    @classmethod
    def test_read_dishes_after_delete(cls):
        response = client.get(reverse('get_all_dishes', menu_id=cls.menu_id, submenu_id=cls.submenu_id))
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    @classmethod
    def test_read_menu_after_delete_submenu(cls):
        response = client.get(reverse('get_menu', id=cls.menu_id))
        assert response.status_code == 200
        data = response.json()
        assert 'id' in data
        assert data['dishes_count'] == 0
        assert data['submenus_count'] == 0

    @classmethod
    def test_delete_menu(cls):
        response = client.delete(reverse('delete_menu', id=cls.menu_id))
        assert response.status_code == 200
        assert not response.json()

    @classmethod
    def test_read_menus(cls):
        response = client.get(reverse('get_all_menus'))
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
