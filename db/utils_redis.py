import uuid

from sqlalchemy.orm import Session

from db.models import Dish, Submenu


def get_submenu_id_for_dish(db: Session, id: uuid.UUID | None = None) -> uuid.UUID | None:
    # Получение идентификатора подменю для удаляемого блюда из основной базы данных
    dish = db.query(Dish).filter(Dish.id == id).first()
    if dish:
        return dish.submenu_id
    return None


def get_menu_id_for_submenu(db: Session, id: uuid.UUID | None = None) -> uuid.UUID | None:
    # Получение идентификатора меню для указанного подменю из основной базы данных
    submenu = db.query(Submenu).filter(Submenu.id == id).first()
    if submenu:
        return submenu.menu_id
    return None
