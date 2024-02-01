import logging
import uuid
from typing import List, Any, NoReturn, Optional

from sqlalchemy import func, Row, Boolean
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import schemas
from db.models import Menu, Submenu, Dish


class CRUDRestaurantService:
    """ALL ORM METHODS."""

    def __init__(self, model):
        self.model = model

    def create(
            self,
            data: schemas.Menu | schemas.Submenu | schemas.Dish,
            db: Session,
            menu_id: uuid.UUID = None,
            submenu_id: uuid.UUID = None,
            id: uuid.UUID = None
    ) -> Optional[List[Row[tuple[Any]]], Boolean]:
        table = self.model(**data.model_dump())
        if id is not None:
            table.id = id
        if menu_id is not None:
            table.menu_id = menu_id
        if submenu_id is not None:
            table.submenu_id = submenu_id
        try:
            db.add(table)
            db.commit()
            db.refresh(table)
        except IntegrityError as e:
            logging.info(e)
            return False
        return table

    def read(
            self,
            db: Session,
            id: uuid.UUID = None,
    ) -> Row[tuple[Any]]:
        if id:
            result = db.query(self.model).filter(self.model.id == id).first()
            if self.model == Menu and result is not None:
                query = db.query(
                    Menu.id,
                    func.count(Submenu.id.distinct()).label('submenus_count'),
                    func.count(Dish.id.distinct()).label('dishes_count')
                ).select_from(Menu).outerjoin(Submenu).outerjoin(Dish).group_by(Menu.id)
                result_menu = query.first()
                result.submenus_count = result_menu[1]
                result.dishes_count = result_menu[2]
            elif self.model == Submenu and result is not None:
                query = db.query(
                    Submenu.id,
                    func.count(Dish.id.distinct()).label('dishes_count')
                ).select_from(Submenu).outerjoin(Dish, Submenu.id == Dish.submenu_id).group_by(Submenu.id)
                result_submenu = query.first()
                result.dishes_count = result_submenu[1]
            return result

    def read_all(
            self,
            db: Session
    ) -> List[Row[tuple[Any]]]:
        return db.query(self.model).all()

    def update(
            self,
            data: schemas.Menu | schemas.Submenu | schemas.Dish,
            db: Session,
            id: uuid.UUID = None
    ) -> Row[tuple[Any]]:
        table = db.query(self.model).filter(self.model.id == id).first()
        for key, value in data.model_dump().items():
            setattr(table, key, value)
        try:
            db.add(table)
            db.commit()
            db.refresh(table)
        except IntegrityError as e:
            logging.info(e)
        return table

    def delete(
            self,
            db: Session,
            id: uuid.UUID = None
    ) -> NoReturn:
        db.query(self.model).filter(self.model.id == id).delete()
        db.commit()
