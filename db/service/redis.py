import json
import uuid
from typing import Any

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Row
from sqlalchemy.orm import Session

from core import re
from db import schemas
from db.database import get_db
from db.models import Dish, Menu, Submenu
from db.service.postgres import CRUDRestaurantService
from db.utils_redis import get_menu_id_for_submenu, get_submenu_id_for_dish


class CRUDRedisService:
    def __init__(
            self,
            model
    ):
        self.model = model
        self.restaurant_service = CRUDRestaurantService(self.model)
        self.db: Session = Depends(get_db)

    def store(
            self,
            item: Menu | Submenu | Dish
    ) -> None:
        """Сохранение данных"""
        item_str = json.dumps(jsonable_encoder(item))
        re.set(f'{self.model}:{item.id}', item_str)
        re.expire(f'{self.model}:{item.id}', 60)

    def read(
            self,
            id: uuid.UUID | None = None
    ) -> bytes | None:
        """Считываем запись"""
        result_redis = re.get(f'{self.model}:{id}')
        if result_redis is not None:
            return result_redis
        else:
            result = self.restaurant_service.read(id)
            if result is not None:
                re.set(f'{self.model}:{id}', json.dumps(jsonable_encoder(result)))
                re.expire(f'{self.model}:{id}', 60)
        return None

    def read_all(
            self
    ) -> list[dict[str, str | int]]:
        """Считываем записи"""
        items = []
        for key in re.scan_iter(f'{self.model}:*'):
            result_redis = re.get(key)
            if result_redis is not None:
                items.append(json.loads(result_redis.decode('utf-8')))
        return items

    def update(
            self,
            id: uuid.UUID,
            data: schemas.Menu | schemas.Submenu | schemas.Dish,
    ) -> Row[tuple[Any]]:
        """Обновление данных"""
        updated_item = self.restaurant_service.update(data, id)
        if updated_item:
            item_str = json.dumps(jsonable_encoder(updated_item))
            if 'price' in item_str:
                updated_item.price = str(updated_item.price)
                item_str = json.dumps(jsonable_encoder(updated_item))
            re.set(f'{self.model}:{id}', item_str)
            re.expire(f'{self.model}:{id}', 60)
            return updated_item
        else:
            raise HTTPException(status_code=404, detail='Item not found')

    def delete(
            self,
            id: uuid.UUID,
    ) -> None:
        """Удаление всех данных"""
        menu = Menu
        if self.model == Dish:
            re.delete(f'{self.model}: {id}')
            submenu_id = get_submenu_id_for_dish(self.db, id)
            if submenu_id:
                submenu = Submenu
                re.delete(f'{submenu}:{submenu_id}')
                menu_id = get_menu_id_for_submenu(self.db, submenu_id)
                if menu_id:
                    re.delete(f'{menu}:{menu_id}')
        elif self.model == Submenu:
            re.delete(f'{self.model}:{id}')
            menu_id = get_menu_id_for_submenu(self.db, id)
            if menu_id:
                re.delete(f'{menu}:{menu_id}')
        re.delete(f'{self.model}:{id}')
