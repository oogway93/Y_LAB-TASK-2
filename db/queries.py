import logging
import uuid

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import schemas
from db.database import Base, engine
from db.models import Menu, Submenu, Dish


class CRUDRestaurantService:
    """ALL ORM METHODS."""

    def __init__(self, model):
        self.model = model

    @staticmethod
    def create_tables():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    def create(
            self,
            data: schemas.Menu | schemas.Submenu | schemas.Dish,
            db: Session,
            menu_id: uuid.UUID = None,
            submenu_id: uuid.UUID = None,
            id: uuid.UUID = None
    ):
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
    ):
        if id:
            result = db.query(self.model).filter(self.model.id == id).first()
            if self.model == Menu and result is not None:
                query = db.query(
                    Menu.id,
                    Menu.title,
                    Menu.description,
                    func.count(Submenu.id.distinct()).label('submenus_count'),
                    func.count(Dish.id.distinct()).label('dishes_count')
                ).select_from(Menu).outerjoin(Submenu).outerjoin(Dish).group_by(Menu.id)
                result_menu = query.first()
                result_dict = {
                    'id': str(result_menu[0]),
                    'title': result_menu[1],
                    'description': result_menu[2],
                    'submenus_count': result_menu[3],
                    'dishes_count': result_menu[4]
                }
                return result_dict
            elif self.model == Submenu and result is not None:
                query = db.query(
                    Submenu.id,
                    Submenu.title,
                    Submenu.description,
                    func.count(Dish.id.distinct()).label('dishes_count')
                ).select_from(Submenu).outerjoin(Dish, Submenu.id == Dish.submenu_id).group_by(Submenu.id)
                result_submenu = query.first()
                result_dict = {
                    'id': str(result_submenu[0]),
                    'title': result_submenu[1],
                    'description': result_submenu[2],
                    'dishes_count': result_submenu[3]
                }
                return result_dict
            return result

    def read_all(
            self,
            db: Session
    ):
        return db.query(self.model).all()

    def update(
            self,
            data: schemas.Menu | schemas.Submenu | schemas.Dish,
            db: Session,
            id: uuid.UUID = None
    ):
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
    ):
        db.query(self.model).filter(self.model.id == id).delete()
        db.commit()
