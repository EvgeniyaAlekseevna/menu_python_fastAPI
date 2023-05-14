import uuid
from .database import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    submenus_count = Column(Integer, default=0)
    dishes_count = Column(Integer, default=0)


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    dishes_count = Column(Integer, default=0)

    menu = relationship("Menu")
    menu_id = Column(UUID(as_uuid=True),
                     ForeignKey("menus.id", ondelete="CASCADE"),
                     nullable=False)


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(Float)

    submenu = relationship("Submenu")
    submenu_id = Column(UUID(as_uuid=True),
                        ForeignKey("submenus.id", ondelete="CASCADE"),
                        nullable=False)
