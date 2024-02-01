import uvicorn
from fastapi import FastAPI

from db.queries import CRUDRestaurantService
from handlers.handlers_dish import router as dish_router
from handlers.handlers_menu import router as menu_router
from handlers.handlers_submenu import router as submenu_router

app = FastAPI(title='Task 2')
app.include_router(menu_router)
app.include_router(submenu_router)
app.include_router(dish_router)


def main():
    CRUDRestaurantService.create_tables()


if __name__ == '__main__':
    main()
    uvicorn.run('core:app', reload=True)
