from typing import List, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..database import get_db
from ..models import Dish, Submenu, Menu
from ..schemas import DishSchemaBase, DishShema

router = APIRouter()


@router.get('/')
def view_the_dish_list(db: Session = Depends(get_db)
                       ) -> List[DishShema]:
    dish_view = db.query(Dish).all()
    return dish_view


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_a_dish(target_submenu_id: UUID,
                  dish: DishSchemaBase,
                  db: Session = Depends(get_db)
                  ) -> DishShema:
    new_dish = Dish(**dish.dict())
    new_dish.submenu_id = target_submenu_id
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    update_submenu = db.query(Submenu).filter(Submenu.id == new_dish.submenu_id).first()
    update_submenu.dishes_count += 1
    db.commit()
    db.refresh(update_submenu)
    update_menu = db.query(Menu).filter(Menu.id == update_submenu.menu_id).first()
    update_menu.dishes_count += 1
    db.commit()
    db.refresh(update_menu)
    return new_dish


@router.get('/{target_dish_id}')
def target_dish_id(target_dish_id: UUID,
                   db: Session = Depends(get_db)
                   ) -> DishShema:
    db_dish = db.query(Dish).filter(Dish.id == target_dish_id).first()
    if not db_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    return db_dish


@router.patch('/{target_dish_id}')
def refresh_submenu(target_dish_id: UUID,
                    dish: DishSchemaBase,
                    db: Session = Depends(get_db)
                    ) -> DishShema:
    filter_dish = db.query(Dish).filter(Dish.id == target_dish_id)
    db_dish = filter_dish.first()
    if not db_dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    filter_dish.update(dish.dict(exclude_unset=True))
    db.commit()
    db.refresh(db_dish)
    return db_dish


@router.delete('/{target_dish_id}')
def delete_submenu(target_dish_id: UUID,
                   db: Session = Depends(get_db)
                   ) -> Dict:
    filter_dish = db.query(Dish).filter(Dish.id == target_dish_id).first()
    db.delete(filter_dish)
    db.commit()
    update_submenu = db.query(Submenu).filter(Submenu.id == filter_dish.submenu_id).first()
    update_submenu.dishes_count -= 1
    db.commit()
    db.refresh(update_submenu)
    update_menu = db.query(Menu).filter(Menu.id == update_submenu.menu_id).first()
    update_menu.dishes_count -= 1
    db.commit()
    db.refresh(update_menu)
    return {"status": "true", "message": "The dish has been deleted"}
