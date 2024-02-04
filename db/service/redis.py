import json
import uuid

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core import re
from db import schemas
from db.models import Dish, Menu, Submenu
from db.service.postgres import CRUDRestaurantService
from db.utils_redis import get_menu_id_for_submenu, get_submenu_id_for_dish


class CRUDRedisService:
    def __init__(self, model):
        self.model = model
        self.restaurant_service = CRUDRestaurantService(self.model)

    def store(self, item):
        # Convert the item to a JSON-encoded string
        # if item == Dish:
        #     item.price = str(float(item.price))
        item_str = json.dumps(jsonable_encoder(item))
        # Store the item in Redis with a key based on its ID
        re.set(f'{self.model}:{item.id}', item_str)
        re.expire(f'{self.model}:{item.id}', 60)

    def read(self, db: Session, id: uuid.UUID | None = None):
        result_redis = re.get(f'{self.model}:{id}')
        if result_redis is not None:
            return result_redis
        else:
            result = self.restaurant_service.read(db, id)
            if result is not None:
                re.set(f'{self.model}:{id}', json.dumps(jsonable_encoder(result)))
                re.expire(f'{self.model}:{id}', 60)

    def read_all(self):
        items = []
        for key in re.scan_iter(f'{self.model}:*'):
            result_redis = re.get(key)
            if result_redis is not None:
                # result_redis['price'] = str(result_redis['price'])
                items.append(json.loads(result_redis.decode('utf-8')))
        return items

    def update(self, id: uuid.UUID, data: schemas.Menu | schemas.Submenu | schemas.Dish, db: Session) -> dict | None:
        """Updates an item in Redis and the database"""
        # First, update the item in the database
        updated_item = self.restaurant_service.update(data, db, id)
        if updated_item:
            # Then, update the item in Redis

            item_str = json.dumps(jsonable_encoder(updated_item))
            if 'price' in item_str:
                updated_item.price = str(updated_item.price)
                item_str = json.dumps(jsonable_encoder(updated_item))
            re.set(f'{self.model}:{id}', item_str)
            re.expire(f'{self.model}:{id}', 60)
            return updated_item
        else:
            # Handle the case where the item was not found in the database
            raise HTTPException(status_code=404, detail='Item not found')

    def delete(self, id: uuid.UUID, db: Session) -> None:
        """Deletes an item from Redis"""
        menu = Menu
        if self.model == Dish:
            re.delete(f'{self.model}: {id}')
            submenu_id = get_submenu_id_for_dish(db, id)
            if submenu_id:
                # Удаление кеша для подменю
                submenu = Submenu
                re.delete(f'{submenu}:{submenu_id}')

                # Получение идентификатора меню через подменю
                menu_id = get_menu_id_for_submenu(db, submenu_id)
                if menu_id:
                    # Удаление кеша для меню
                    re.delete(f'{menu}:{menu_id}')
        elif self.model == Submenu:
            re.delete(f'{self.model}:{id}')
            menu_id = get_menu_id_for_submenu(db, id)
            if menu_id:
                re.delete(f'{menu}:{menu_id}')
        re.delete(f'{self.model}:{id}')
