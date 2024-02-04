import uuid

from fastapi import Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Dish, Submenu


def get_submenu_id_for_dish(db: Session = Depends(get_db), id: uuid.UUID | None = None) -> uuid.UUID | None:
    # Получение идентификатора подменю для удаляемого блюда из основной базы данных
    dish = db.query(Dish).filter(Dish.id == id).first()
    if dish:
        return dish.submenu_id
    return None


def get_menu_id_for_submenu(db: Session = Depends(get_db), id: uuid.UUID | None = None) -> uuid.UUID | None:
    # Получение идентификатора меню для указанного подменю из основной базы данных
    submenu = db.query(Submenu).filter(Submenu.id == id).first()
    if submenu:
        return submenu.menu_id
    return None
