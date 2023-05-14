from typing import List, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..database import get_db
from ..models import Menu, Submenu, Dish
from ..schemas import MenuSchemaBase,SubmenuSchema

router = APIRouter()

@router.get('/')
def view_the_submenu_list(db: Session = Depends(get_db)
                          ) -> List[SubmenuSchema]:
    submenu_view = db.query(Submenu).all()
    return submenu_view


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_a_submenu(target_menu_id: UUID,
                     submenu: MenuSchemaBase,
                     db: Session = Depends(get_db)
                     ) -> SubmenuSchema:
    new_submenu = Submenu(**submenu.dict())
    new_submenu.menu_id = target_menu_id
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    update_menu = db.query(Menu).filter(Menu.id == new_submenu.menu_id).first()
    update_menu.submenus_count += 1
    db.commit()
    db.refresh(update_menu)
    return new_submenu


@router.get('/{target_submenu_id}')
def target_submenu_id(target_submenu_id: UUID,
                      db: Session = Depends(get_db)
                      ) -> SubmenuSchema:
    db_submenu = db.query(Submenu).filter(Submenu.id == target_submenu_id).first()
    if not db_submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    return db_submenu


@router.patch('/{target_submenu_id}')
def refresh_submenu(target_submenu_id: UUID,
                    submenu: MenuSchemaBase,
                    db: Session = Depends(get_db)
                    ) -> SubmenuSchema:
    filter_submenu = db.query(Submenu).filter(Submenu.id == target_submenu_id)
    db_submenu = filter_submenu.first()
    if not db_submenu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    filter_submenu.update(submenu.dict(exclude_unset=True))
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


@router.delete('/{target_submenu_id}')
def delete_submenu(target_submenu_id: UUID,
                   db: Session = Depends(get_db)
                   ) -> Dict:
    filter_submenu = db.query(Submenu).filter(Submenu.id == target_submenu_id).first()
    db.delete(filter_submenu)
    db.commit()
    update_menu = db.query(Menu).filter(Menu.id == filter_submenu.menu_id).first()
    update_menu.submenus_count -=1
    update_menu.dishes_count -= filter_submenu.dishes_count
    db.commit()
    db.refresh(update_menu)
    delete_dish = db.query(Dish).filter(Dish.submenu_id == target_submenu_id)
    for item in delete_dish:
        db.delete(item)
        db.commit()
    return {"status": "true", "message": "The submenu has been deleted"}