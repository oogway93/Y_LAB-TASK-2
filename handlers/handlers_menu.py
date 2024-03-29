import json
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from db import schemas
from db.models import Menu
from service.postgres import CRUDRestaurantService
from service.redis import CRUDRedisService

router = APIRouter(prefix='/api/v1', tags=['Menu'])

restaurant_service = CRUDRestaurantService(Menu)
redis_service = CRUDRedisService(Menu)


@router.post('/menus')
async def create_menu(
        data: schemas.Menu,
) -> JSONResponse:
    """Создаёт меню"""
    menu_creation = restaurant_service.create(data)
    if not menu_creation:
        return JSONResponse(content={'Error': 'Creation menu is failed'}, status_code=400)
    json_compatible_item_data = jsonable_encoder(menu_creation)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get('/menus/{id}', response_model=schemas.Menu)
async def get_menu(
        id: uuid.UUID,
) -> JSONResponse:
    """Просматривает определенное меню"""
    cached_menu = redis_service.read(id)
    if cached_menu is not None:
        return JSONResponse(content=json.loads(cached_menu.decode('utf-8')))
    menu = restaurant_service.read(id)
    if not menu:
        return JSONResponse(content={'detail': 'menu not found'}, status_code=404)
    json_compatible_item_data = jsonable_encoder(menu)
    return JSONResponse(content=json_compatible_item_data)


@router.get('/menus')
async def get_all_menus(
) -> list[dict[str, str | int]] | list[schemas.Menu]:
    """Просматривает список меню"""
    cached_menus = redis_service.read_all()
    if cached_menus:
        return cached_menus
    else:
        menus_in_db = restaurant_service.read_all()

        for menu in menus_in_db:
            redis_service.store(menu)

        return menus_in_db


@router.patch('/menus/{id}')
async def update_menu(
        id: uuid.UUID,
        data: schemas.Menu,
) -> JSONResponse:
    """Обновляет меню"""
    try:
        updated_menu = redis_service.update(id, data)
        return JSONResponse(content=jsonable_encoder(updated_menu))
    except HTTPException as e:
        raise e


@router.delete('/menus/{id}')
async def delete_menu(
        id: uuid.UUID,
) -> None:
    """Удаляет меню"""
    redis_service.delete(id)
    return restaurant_service.delete(id)
