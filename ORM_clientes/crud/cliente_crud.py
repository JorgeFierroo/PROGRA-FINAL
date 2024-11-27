from sqlalchemy.orm import Session
from models import Cliente

class ClienteCRUD:
    @staticmethod

    def crear_cliente(db: Session, nombre: str, correo: str, edad: int):
        cliente_existente = db.query(Cliente).filter_by(correo=correo).first()
        if cliente_existente:
            print(f"El cliente con correo '{correo}' ya existe.")
            return cliente_existente

        cliente = Cliente(nombre=nombre, correo=correo)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        print(f"Cliente '{nombre}' agregado exitosamente.")
        return cliente

    @staticmethod
    def leer_clientes(db: Session):
        return db.query(Cliente).all()

    @staticmethod
    def actualizar_cliente(db: Session, cliente_id: int, nuevo_nombre: str = None, nuevo_correo: str = None, edad: int = None):
        cliente = db.query(Cliente).filter_by(id=cliente_id).first()
        if not cliente:
            print(f"Cliente con ID '{cliente_id}' no encontrado.")
            return None

        if nuevo_nombre:
            cliente.nombre = nuevo_nombre
        if nuevo_correo:
            cliente_existente = db.query(Cliente).filter_by(correo=nuevo_correo).first()
            if cliente_existente and cliente_existente.id != cliente_id:
                print(f"El correo '{nuevo_correo}' ya está en uso por otro cliente.")
                return None
            cliente.correo = nuevo_correo

        db.commit()
        db.refresh(cliente)
        print(f"Cliente con ID '{cliente_id}' actualizado exitosamente.")
        return cliente

    @staticmethod
    def eliminar_cliente(db: Session, cliente_id: int):
        cliente = db.query(Cliente).filter_by(id=cliente_id).first()
        if not cliente:
            print(f"Cliente con ID '{cliente_id}' no encontrado.")
            return None

        db.delete(cliente)
        db.commit()
        print(f"Cliente con ID '{cliente_id}' eliminado exitosamente.")
        return cliente
