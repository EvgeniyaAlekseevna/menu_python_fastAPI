from typing import Dict, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from ..database import get_db
from ..models import Menu
from ..schemas import MenuSchemaBase, MenuSchema

router = APIRouter()


@router.get('/')
def view_the_menu_list(db: Session = Depends(get_db)
                       ) -> List[MenuSchema]:
    menu_view = db.query(Menu).all()
    return menu_view


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_a_menu(menu: MenuSchemaBase,
                  db: Session = Depends(get_db)
                  ) -> MenuSchema:
    new_menu = Menu(**menu.dict())
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


@router.get('/{target_menu_id}')
def target_menu_id(target_menu_id: UUID,
                   db: Session = Depends(get_db)
                   )-> MenuSchema:
    db_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    if not db_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail = "menu not found"
        )
    else:
        return db_menu


@router.patch('/{target_menu_id}')
def refresh_menu(target_menu_id: UUID,
                 menu: MenuSchemaBase,
                 db: Session = Depends(get_db)
                 )-> MenuSchema:
    filter_menu = db.query(Menu).filter(Menu.id == target_menu_id)
    db_menu = filter_menu.first()
    if not filter_menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    filter_menu.update(menu.dict(exclude_unset=True))
    db.commit()
    db.refresh(db_menu)
    return db_menu


@router.delete('/{target_menu_id}')
def delete_menu(target_menu_id: UUID,
                db: Session = Depends(get_db)
                ) -> Dict:
    filter_menu = db.query(Menu).filter(Menu.id == target_menu_id).first()
    db.delete(filter_menu)
    db.commit()
    return {"status": "true", "message": "The menu has been deleted"}

