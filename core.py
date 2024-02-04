import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import REDIS_HOST

REDIS_HOST: str | None = REDIS_HOST

# Проверяем, определена ли переменная REDIS_HOST
if REDIS_HOST is not None:
    # Переменная определена, инициализируем Redis с переданным хостом
    re = redis.Redis(host=REDIS_HOST, port=6379)
else:
    # Переменная не определена, используем значение по умолчанию
    re = redis.Redis(host='localhost', port=6379)


def create_app():
    from handlers.handlers_dish import router as dish_router
    from handlers.handlers_menu import router as menu_router
    from handlers.handlers_submenu import router as submenu_router
    app = FastAPI(title='Task 3', version='0.3.0')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
    app.include_router(menu_router)
    app.include_router(submenu_router)
    app.include_router(dish_router)
    return app


app = create_app()
