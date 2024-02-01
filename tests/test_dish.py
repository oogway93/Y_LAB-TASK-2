from fastapi.testclient import TestClient

from core import app
from tests.utils import reverse

client = TestClient(app)


class TestDish:
    """Test Class Dish"""
    menu_id: str = ''
    submenu_id: str = ''
    id: str = ''

    @classmethod
    def test_create_menu(cls):
        data = {
            'title': 'My menu 1',
            'description': 'My menu description 1'
        }
        response = client.post(reverse('create_menu'), json=data)
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
        response = client.post(reverse('create_submenu', menu_id=cls.menu_id), json=data)
        assert response.status_code == 201
        response_data = response.json()
        cls.submenu_id = response_data['id']
        assert 'id' in response_data
        assert response_data['title'] == data['title']
        assert response_data['description'] == data['description']

    @classmethod
    def test_create_dish(cls):
        data = {
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50'
        }
        response = client.post(reverse('create_dish', menu_id=cls.menu_id, submenu_id=cls.submenu_id), json=data)
        assert response.status_code == 201
        response_data = response.json()
        cls.id = response_data['id']
        assert 'id' in response_data
        assert response_data['title'] == data['title']
        assert response_data['description'] == data['description']
        assert response_data['price'] == data['price'][:-1]

    @classmethod
    def test_read_dish(cls):
        response = client.get(reverse('get_dish', menu_id=cls.menu_id, submenu_id=cls.submenu_id, id=cls.id))
        assert response.status_code == 200
        response_data = response.json()
        assert 'id' in response_data
        assert response_data['title'] == 'My dish 1'
        assert response_data['description'] == 'My dish description 1'
        assert response_data['price'] == '12.5'

    @classmethod
    def test_read_dishes(cls):
        response = client.get(reverse('get_all_dishes', menu_id=cls.menu_id, submenu_id=cls.submenu_id))
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 1
        assert response_data[0]['title'] == 'My dish 1'
        assert response_data[0]['description'] == 'My dish description 1'
        assert response_data[0]['price'] == 12.5

    @classmethod
    def test_update_dish(cls):
        updated_data = {
            'title': 'My updated dish 1',
            'description': 'My updated dish description 1',
            'price': '14.50'
        }
        response = client.patch(reverse('update_dish', menu_id=cls.menu_id, submenu_id=cls.submenu_id, id=cls.id),
                                json=updated_data)
        assert response.status_code == 200
        response_data = response.json()
        assert 'id' in response_data
        assert response_data['title'] == updated_data['title']
        assert response_data['description'] == updated_data['description']
        assert response_data['price'] == updated_data['price'][:-1]

    @classmethod
    def test_delete_dish(cls):
        response = client.delete(reverse('delete_dish', menu_id=cls.menu_id, submenu_id=cls.submenu_id, id=cls.id))
        assert response.status_code == 200
        assert not response.json()

    @classmethod
    def test_delete_submenu(cls):
        response = client.delete(reverse('delete_submenu', menu_id=cls.menu_id, id=cls.submenu_id))
        assert response.status_code == 200
        assert not response.json()

    @classmethod
    def test_delete_menu(cls):
        response = client.delete(reverse('delete_menu', id=cls.menu_id))
        assert response.status_code == 200
        assert not response.json()
