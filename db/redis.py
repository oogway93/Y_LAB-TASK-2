import json
import uuid

from fastapi.encoders import jsonable_encoder
from redis_om import NotFoundError
from sqlalchemy.orm import Session

from core import redis
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
