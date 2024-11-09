from sqlalchemy.orm import Session
from models import Producto, Cliente, Orden
from schemas import ProductoCreate, ClienteCreate, OrdenCreate

def get_productos(db: Session):
    return db.query(Producto).all()

def create_producto(db: Session, producto: ProductoCreate):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Funciones similares para clientes y órdenes
