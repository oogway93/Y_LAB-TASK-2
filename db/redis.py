import json
import uuid

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from redis_om import NotFoundError
from sqlalchemy.orm import Session

from core import redis
from db import schemas
from db.queries import CRUDRestaurantService


class CRUDRedisService:
    def __init__(self, model):
        self.model = model
        self.restaurant_service = CRUDRestaurantService(self.model)

    def store(self, item):
        # Convert the item to a JSON-encoded string
        item_str = json.dumps(jsonable_encoder(item))
        # Store the item in Redis with a key based on its ID
        redis.set(f'{self.model}:{item.id}', item_str)

    def read(self, db: Session, id: uuid.UUID | None = None):
        try:
            result_redis = redis.get(f'{self.model}:{id}')
            return result_redis
        except NotFoundError:
            result = self.restaurant_service.read(db, id)
            redis.set(f'{self.model}:{id}', json.dumps(jsonable_encoder(result)))

    def read_all(self):
        menus = []
        for key in redis.scan_iter(f'{self.model}:*'):
            result_redis = redis.get(key)
            if result_redis is not None:
                menus.append(json.loads(result_redis.encode('utf-8')))
        return menus

    def update(self, id: uuid.UUID, data: schemas.Menu | schemas.Submenu | schemas.Dish, db: Session) -> dict | None:
        """Updates an item in Redis and the database"""
        # First, update the item in the database
        updated_item = self.restaurant_service.update(data, db, id)
        if updated_item:
            # Then, update the item in Redis
            item_str = json.dumps(jsonable_encoder(updated_item))
            redis.set(f'{self.model}:{id}', item_str)
            return updated_item
        else:
            # Handle the case where the item was not found in the database
            raise HTTPException(status_code=404, detail='Item not found')

    def delete(self, id: uuid.UUID) -> None:
        """Deletes an item from Redis"""
        # Construct the key for the item to be deleted
        key = f'{self.model}:{id}'
        # Delete the key from Redis
        redis.delete(key)
