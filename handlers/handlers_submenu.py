import json
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from db import schemas
from db.models import Submenu
from service.postgres import CRUDRestaurantService
from service.redis import CRUDRedisService

router = APIRouter(prefix='/api/v1/menus', tags=['Submenu'])

restaurant_service = CRUDRestaurantService(Submenu)
redis_service = CRUDRedisService(Submenu)


@router.post('/{menu_id}/submenus')
async def create_submenu(
        menu_id: uuid.UUID, data: schemas.Submenu,
) -> JSONResponse:
    """Создаёт подменю"""
    submenu_creation = restaurant_service.create(data, menu_id=menu_id)
    if not submenu_creation:
        return JSONResponse(content={'Error': 'Creation submenu is failed'}, status_code=400)
    json_compatible_item_data = jsonable_encoder(submenu_creation)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get('/{menu_id}/submenus/{id}', response_model=schemas.Submenu)
async def get_submenu(
        id: uuid.UUID,
) -> JSONResponse:
    """Просматривает определенное подменю"""
    cached_submenu = redis_service.read(id)
    if cached_submenu is not None:
        return JSONResponse(content=json.loads(cached_submenu.decode('utf-8')))
    submenu = restaurant_service.read(id)
    if not submenu:
        return JSONResponse(content={'detail': 'submenu not found'}, status_code=404)
    json_compatible_item_data = jsonable_encoder(submenu)
    return JSONResponse(content=json_compatible_item_data)


@router.get('/{menu_id}/submenus')
async def get_all_submenus(
) -> list[dict[str, str | int]] | list[schemas.Submenu]:
    """Просматривает список подменю"""
    cached_submenus = redis_service.read_all()
    if cached_submenus:
        return cached_submenus
    else:
        submenus_in_db = restaurant_service.read_all()

        for submenu in submenus_in_db:
            redis_service.store(submenu)

        return submenus_in_db


@router.patch('/{menu_id}/submenus/{id}')
async def update_submenu(
        id: uuid.UUID,
        data: schemas.Submenu,
) -> JSONResponse:
    """Обновляет подменю"""
    try:
        updated_submenu = redis_service.update(id, data)
        return JSONResponse(content=jsonable_encoder(updated_submenu))
    except HTTPException as e:
        raise e


@router.delete('/{menu_id}/submenus/{id}')
async def delete_submenu(
        id: uuid.UUID,
) -> None:
    """Удаляет подменю"""
    redis_service.delete(id)
    return restaurant_service.delete(id)
