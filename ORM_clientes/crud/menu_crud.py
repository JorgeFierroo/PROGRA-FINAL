from sqlalchemy.orm import Session
from models import Menu

def crear_menu(db:Session,nombre:str,descripcion:str,ingredientes:list):
    menu_existente = db.query(Menu).filter_by(nombre=nombre).first()
    if menu_existente:
        print(f"El menú '{nombre}' ya existe")
        return menu_existente
    
    menu = Menu()




