from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from database import Base

class MenuIngrediente(Base):
    __tablename__ = "menu_ingrediente"
    menu_nombre = Column(String, ForeignKey("menus.nombre"), primary_key=True)
    ingrediente_nombre = Column(String, ForeignKey("ingredientes.nombre"), primary_key=True)
    cantidad = Column(Integer, nullable=False)  # Cantidad de ingrediente

    # Relación inversa para facilitar acceso
    menu = relationship("Menu", back_populates="menu_ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="ingrediente_menus")


class Menu(Base):
    __tablename__ = "menus"
    nombre = Column(String, primary_key=True, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)

    # Relación con la tabla intermedia
    menu_ingredientes = relationship("MenuIngrediente", back_populates="menu")

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    nombre = Column(String, primary_key=True, nullable=False, unique=True)
    tipo = Column(String, nullable=True)
    cantidad = Column(Integer, nullable=False)
    unidad = Column(String, nullable=True)

    # Relación con la tabla intermedia
    ingrediente_menus = relationship("MenuIngrediente", back_populates="ingrediente")
