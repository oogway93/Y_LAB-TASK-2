import logging
import uuid
from typing import Any

from sqlalchemy import Row, func
from sqlalchemy.exc import IntegrityError

from db import schemas
from db.database import Base, SessionLocal, engine
from db.models import Dish, Menu, Submenu


class CRUDRestaurantService:
    """ALL ORM METHODS."""

    @staticmethod
    def create_tables():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def __init__(self, model):
        self.model = model
        self.db = SessionLocal()

    def create(
            self,
            data: schemas.Menu | schemas.Submenu | schemas.Dish,
            menu_id: uuid.UUID | None = None,
            submenu_id: uuid.UUID | None = None,
            id: uuid.UUID | None = None
    ) -> bool:
        """Создание"""
        table = self.model(**data.model_dump())
        if id is not None:
            table.id = id
        if menu_id is not None:
            table.menu_id = menu_id
        if submenu_id is not None:
            table.submenu_id = submenu_id
        try:
            self.db.add(table)
            self.db.commit()
            self.db.refresh(table)
        except IntegrityError as e:
            logging.info(e)
            return False
        return table

    def read(
            self,
            id: uuid.UUID | None = None,
    ) -> schemas.Menu | schemas.Submenu | schemas.Dish | Row[tuple[Any]] | None:
        """Запись"""
        result = self.db.query(self.model).filter(self.model.id == id).first()
        if self.model == Menu and result is not None:
            query = self.db.query(
                Menu.id,
                func.count(Submenu.id.distinct()).label('submenus_count'),
                func.count(Dish.id.distinct()).label('dishes_count')
            ).select_from(Menu).outerjoin(Submenu).outerjoin(Dish).group_by(Menu.id)
            result_menu = query.first()
            result.submenus_count = result_menu[1]
            result.dishes_count = result_menu[2]
        elif self.model == Submenu and result is not None:
            query = self.db.query(
                Submenu.id,
                func.count(Dish.id.distinct()).label('dishes_count')
            ).select_from(Submenu).outerjoin(Dish).group_by(Submenu.id)
            result_submenu = query.first()
            result.dishes_count = result_submenu[1]
        return result

    def read_all(
            self,
    ) -> list[schemas.Menu | schemas.Submenu | schemas.Dish] | list[Row[tuple[Any]]]:
        """Все записи"""
        return self.db.query(self.model).all()

    def update(
            self,
            data: schemas.Menu | schemas.Submenu | schemas.Dish,
            id: uuid.UUID | None = None
    ) -> Row[tuple[Any]]:
        """Обновление"""
        table = self.db.query(self.model).filter(self.model.id == id).first()
        for key, value in data.model_dump().items():
            setattr(table, key, value)
        try:
            self.db.add(table)
            self.db.commit()
            self.db.refresh(table)
        except IntegrityError as e:
            logging.info(e)
        return table

    def delete(
            self,
            id: uuid.UUID | None = None
    ) -> None:
        """Удаление"""
        self.db.query(self.model).filter(self.model.id == id).delete()
        self.db.commit()

    def __del__(self):
        self.db.close()
