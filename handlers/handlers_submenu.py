import uuid

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db import schemas
from db.database import get_db
from db.models import Submenu
from db.queries import CRUDRestaurantService

router = APIRouter(prefix='/api/v1/menus', tags=['Submenu'])

restaurant_service = CRUDRestaurantService(Submenu)


@router.post('/{menu_id}/submenus')
async def create_submenu(menu_id: uuid.UUID, data: schemas.Submenu,
                         db: Session = Depends(get_db)) -> JSONResponse:
    """Создаёт подменю"""
    submenu_creation = restaurant_service.create(data, db, menu_id)
    if not submenu_creation:
        return JSONResponse(content={'Error': 'Creation menu is failed'}, status_code=400)
    json_compatible_item_data = jsonable_encoder(submenu_creation)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get('/{menu_id}/submenus/{id}', response_model=schemas.Submenu)
async def get_submenu(id: uuid.UUID, db: Session = Depends(get_db)) -> JSONResponse:
    """Просматривает определенное подменю"""
    submenu = restaurant_service.read(db, id)
    if not submenu:
        return JSONResponse(content={'detail': 'submenu not found'}, status_code=404)
    json_compatible_item_data = jsonable_encoder(submenu)
    return JSONResponse(content=json_compatible_item_data)


@router.get('/{menu_id}/submenus')
async def get_all_submenus(db: Session = Depends(get_db)) -> list[schemas.Submenu]:
    """Просматривает список подменю"""
    return restaurant_service.read_all(db)


@router.patch('/{menu_id}/submenus/{id}')
async def update_submenu(id: uuid.UUID, data: schemas.Submenu, db: Session = Depends(get_db)) -> JSONResponse:
    """Обновляет подменю"""
    updated_submenu = restaurant_service.update(data, db, id)
    json_compatible_item_data = jsonable_encoder(updated_submenu)
    return JSONResponse(content=json_compatible_item_data)


@router.delete('/{menu_id}/submenus/{id}')
async def delete_submenu(id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    """Удаляет подменю"""
    return restaurant_service.delete(db, id)
