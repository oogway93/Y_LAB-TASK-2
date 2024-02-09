import json
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from db import schemas
from db.models import Dish
from db.service.postgres import CRUDRestaurantService
from db.service.redis import CRUDRedisService

router = APIRouter(prefix='/api/v1/menus', tags=['Dish'])

restaurant_service = CRUDRestaurantService(Dish)
redis_service = CRUDRedisService(Dish)


@router.post('/{menu_id}/submenus/{submenu_id}/dishes')
async def create_dish(
        submenu_id: uuid.UUID,
        data: schemas.Dish,
) -> JSONResponse:
    """Создаёт блюдо"""
    dish_creation = restaurant_service.create(data, submenu_id=submenu_id)
    if not dish_creation:
        return JSONResponse(content={'detail': 'Failed to create dish'}, status_code=400)
    json_compatible_item_data = jsonable_encoder(dish_creation)
    json_compatible_item_data['price'] = str(json_compatible_item_data['price'])
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{id}', response_model=schemas.Dish)
async def get_dish(
        id: uuid.UUID,
) -> JSONResponse:
    """Просматривает определенное блюдо"""
    cached_dish = redis_service.read(id)
    if cached_dish is not None:
        return JSONResponse(content=json.loads(cached_dish.decode('utf-8')))
    dish = restaurant_service.read(id)
    if dish is not None:
        dish.price = str(dish.price)
    if not dish:
        return JSONResponse(content={'detail': 'dish not found'}, status_code=404)
    json_compatible_item_data = jsonable_encoder(dish)
    return JSONResponse(content=json_compatible_item_data)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes')
async def get_all_dishes(
) -> list[dict[str, str | int]] | list[schemas.Dish]:
    """Просматривает список блюдо"""
    cached_dish = redis_service.read_all()
    if cached_dish:
        return cached_dish
    else:
        dish_in_db = restaurant_service.read_all()

        for dish in dish_in_db:
            dish.price = str(dish.price)
            redis_service.store(dish)

        return dish_in_db


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{id}')
async def update_dish(
        id: uuid.UUID,
        data: schemas.Dish,
) -> JSONResponse:
    """Обновляет блюдо"""
    try:
        updated_dish = redis_service.update(id, data)
        json_compatible_item_data = jsonable_encoder(updated_dish)
        json_compatible_item_data['price'] = str(json_compatible_item_data['price'])
        return JSONResponse(content=json_compatible_item_data)
    except HTTPException as e:
        raise e


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{id}')
async def delete_dish(
        id: uuid.UUID,
) -> None:
    """Удаляет блюдо"""
    redis_service.delete(id)
    return restaurant_service.delete(id)
