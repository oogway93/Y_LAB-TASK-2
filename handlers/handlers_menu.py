import uuid
from typing import NoReturn, List, Any, Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import Response
from sqlalchemy import Row
from sqlalchemy.orm import Session

from db import schemas
from db.database import get_db
from db.models import Menu
from db.queries import CRUDRestaurantService

router = APIRouter(prefix="/api/v1")

restaurant_service = CRUDRestaurantService(Menu)


@router.post("/menus")
async def create_menu(data: schemas.Menu = None, db: Session = Depends(get_db)) -> Optional[JSONResponse, Response]:
    """Создаёт меню"""
    menu_creation = restaurant_service.create(data, db)
    if not menu_creation:
        return Response(content="Error: Creation menu is failed", status_code=400)
    json_compatible_item_data = jsonable_encoder(menu_creation)
    return JSONResponse(content=json_compatible_item_data, status_code=201)


@router.get("/menus/{id}")
async def get_menu(id: uuid.UUID, db: Session = Depends(get_db)) -> Optional[Row[tuple[Any]], JSONResponse]:
    """Просматривает определенное меню"""
    menu = restaurant_service.read(db, id)
    if not menu:
        return JSONResponse(content={"detail": "menu not found"}, status_code=404)
    return menu


@router.get("/menus")
async def get_all_menus(db: Session = Depends(get_db)) -> List[Row[tuple[Any]]]:
    """Просматривает список меню"""
    return restaurant_service.read_all(db)


@router.patch("/menus/{id}")
async def update_menu(id: uuid.UUID, data: schemas.Menu = None, db: Session = Depends(get_db)) -> JSONResponse:
    """Обновляет меню"""
    updated_menu = restaurant_service.update(data, db, id)
    json_compatible_item_data = jsonable_encoder(updated_menu)
    return JSONResponse(content=json_compatible_item_data)


@router.delete("/menus/{id}")
async def delete_menu(id: uuid.UUID, db: Session = Depends(get_db)) -> NoReturn:
    """Удаляет меню"""
    return restaurant_service.delete(db, id)
