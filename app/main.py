from fastapi import FastAPI
from .routers import menu, submenu, dish


app = FastAPI()

app.include_router(menu.router,
                   tags=['Menu'],
                   prefix='/api/v1/menus')
app.include_router(submenu.router,
                   tags=['Submenu'],
                   prefix='/api/v1/menus/{target_menu_id}/submenus')
app.include_router(dish.router,
                   tags=['Dish'],
                   prefix='/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes')
