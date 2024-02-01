import uuid

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from db import schemas
from db.database import get_db
from db.models import Dish
from db.queries import CRUDRestaurantService

router = APIRouter(prefix='/api/v1/menus', tags=['Dish'])

restaurant_service = CRUDRestaurantService(Dish)


@router.post('/{menu_id}/submenus/{submenu_id}/dishes')
async def create_dish(submenu_id: uuid.UUID, data: schemas.Dish,
                      db: Session = Depends(get_db)) -> JSONResponse:
    """Создаёт блюдо"""
    dish_creation = restaurant_service.create(data, db, submenu_id=submenu_id)
    if not dish_creation:
        return JSONResponse(content={'detail': 'Failed to create dish'}, status_code=400)
    json_compatible_item_data = jsonable_encoder(dish_creation)
    json_compatible_item_data['price'] = str(json_compatible_item_data['price'])
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes/{id}', response_model=schemas.Dish)
async def get_dish(id: uuid.UUID, db: Session = Depends(get_db)) -> JSONResponse:
    """Просматривает определенное блюдо"""
    dish = restaurant_service.read(db, id)
    if dish is not None:
        dish.price = str(dish.price)
    if not dish:
        return JSONResponse(content={'detail': 'dish not found'}, status_code=404)
    json_compatible_item_data = jsonable_encoder(dish)
    return JSONResponse(content=json_compatible_item_data)


@router.get('/{menu_id}/submenus/{submenu_id}/dishes')
async def get_all_dishes(db: Session = Depends(get_db)) -> list[schemas.Dish]:
    """Просматривает список блюдо"""
    return restaurant_service.read_all(db)


@router.patch('/{menu_id}/submenus/{submenu_id}/dishes/{id}')
async def update_dish(id: uuid.UUID, data: schemas.Dish, db: Session = Depends(get_db)) -> JSONResponse:
    """Обновляет блюдо"""
    updated_dish = restaurant_service.update(data, db, id)
    json_compatible_item_data = jsonable_encoder(updated_dish)
    json_compatible_item_data['price'] = str(jsonable_encoder(updated_dish)['price'])
    return JSONResponse(content=json_compatible_item_data)


@router.delete('/{menu_id}/submenus/{submenu_id}/dishes/{id}')
async def delete_dish(id: uuid.UUID, db: Session = Depends(get_db)) -> None:
    """Удаляет блюдо"""
    restaurant_service.delete(db, id)
