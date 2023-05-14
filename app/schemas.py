from uuid import UUID
from pydantic import BaseModel

class MenuSchemaBase(BaseModel):
    title: str
    description: str


    class Config:
        orm_mode = True

class MenuSchema(MenuSchemaBase):
    id: UUID
    submenus_count:int
    dishes_count:int

class SubmenuSchema(MenuSchemaBase):
    id: UUID
    dishes_count: int


class DishSchemaBase(MenuSchemaBase):
    price: str

class DishShema(DishSchemaBase):
    id: UUID