import redis
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Task 3', version='0.3.0')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

re: redis.Redis = redis.Redis(host='localhost', port=6379)


@app.on_event('startup')
async def on_startup():
    from handlers.handlers_dish import router as dish_router
    from handlers.handlers_menu import router as menu_router
    from handlers.handlers_submenu import router as submenu_router
    app.include_router(menu_router)
    app.include_router(submenu_router)
    app.include_router(dish_router)


def main():
    from db.queries import CRUDRestaurantService
    CRUDRestaurantService.create_tables()


if __name__ == '__main__':
    main()
    uvicorn.run('core:app', reload=True)
