from fastapi import FastAPI

from handlers.handlers_dish import router as dish_router
from handlers.handlers_menu import router
from handlers.handlers_submenu import router as submenu_router
from db.models import metadata_obj
from db.models import Base

app = FastAPI(title="Task 2")
app.include_router(router)
app.include_router(submenu_router)
app.include_router(dish_router)
