import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db import schemas
from db.database import get_db
from db.models import Submenu
from db.queries import CRUDRestaurantService
from db.redis import CRUDRedisService

router = APIRouter(prefix='/api/v1/menus', tags=['Submenu'])

restaurant_service = CRUDRestaurantService(Submenu)
redis_service = CRUDRedisService(Submenu)


@router.post('/{menu_id}/submenus')
async def create_submenu(menu_id: uuid.UUID, data: schemas.Submenu,
                         db: Session = Depends(get_db)) -> JSONResponse:
    """Создаёт подменю"""
    submenu_creation = restaurant_service.create(data, db, menu_id=menu_id)
    if not submenu_creation:
        return JSONResponse(content={'Error': 'Creation submenu is failed'}, status_code=400)
    # menu_hash = schemas.MenuHash(id=str(), title=data.id,
    #                              description=data.id)
    # menu_hash.save()

    json_compatible_item_data = jsonable_encoder(submenu_creation)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get('/{menu_id}/submenus/{id}', response_model=schemas.Submenu)
async def get_submenu(id: uuid.UUID, db: Session = Depends(get_db)) -> JSONResponse:
    """Просматривает определенное подменю"""
    cached_submenu = redis_service.read(db, id)
    if cached_submenu is not None:
        return JSONResponse(content=json.loads(cached_submenu.decode('utf-8')))
    submenu = restaurant_service.read(db, id)
    if not submenu:
        return JSONResponse(content={'detail': 'submenu not found'}, status_code=404)
    json_compatible_item_data = jsonable_encoder(submenu)
    return JSONResponse(content=json_compatible_item_data)


@router.get('/{menu_id}/submenus')
async def get_all_submenus(db: Session = Depends(get_db)) -> list[schemas.Submenu]:
    """Просматривает список подменю"""
    cached_submenus = redis_service.read_all()
    if cached_submenus:
        return cached_submenus
    else:
        # If no menus are found in Redis, get them from the database
        submenus_in_db = restaurant_service.read_all(db)

        # Store the retrieved menus in Redis for future access
        for submenu in submenus_in_db:
            redis_service.store(submenu)

        return submenus_in_db


@router.patch('/{menu_id}/submenus/{id}')
async def update_submenu(id: uuid.UUID, data: schemas.Submenu, db: Session = Depends(get_db)) -> JSONResponse:
    """Обновляет подменю"""
    try:
        # Attempt to update the menu in Redis and the database
        updated_submenu = redis_service.update(id, data, db)
        return JSONResponse(content=jsonable_encoder(updated_submenu))
    except HTTPException as e:
        # Handle exceptions, such as when the item is not found
        raise e


@router.delete('/{menu_id}/submenus/{id}')
async def delete_submenu(id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    """Удаляет подменю"""
    redis_service.delete(id)
    return restaurant_service.delete(db, id)
