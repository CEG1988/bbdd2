from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Cliente, Categoria, Proveedor, Producto, Orden
from database import SessionLocal  # Asume que tienes una función SessionLocal para obtener la sesión de DB

fake = Faker()

def crear_cliente(db: Session):
    nombre = fake.name()
    email = fake.email()
    cliente = Cliente(nombre=nombre, email=email)
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

def crear_categoria(db: Session):
    nombre = fake.word()
    descripcion = fake.text()
    categoria = Categoria(nombre=nombre, descripcion=descripcion)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

def crear_proveedor(db: Session):
    nombre = fake.company()
    contacto = fake.name()
    telefono = fake.phone_number()
    proveedor = Proveedor(nombre=nombre, contacto=contacto, telefono=telefono)
    db.add(proveedor)
    db.commit()
    db.refresh(proveedor)
    return proveedor

def crear_producto(db: Session, categoria_id: int, proveedor_id: int):
    nombre = fake.word()
    descripcion = fake.text()
    precio = fake.random_number(digits=2)
    cantidad = fake.random_number(digits=2)
    producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, cantidad=cantidad, categoria_id=categoria_id, proveedor_id=proveedor_id)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

def crear_orden(db: Session, cliente_id: int):
    total = fake.random_number(digits=3)
    orden = Orden(cliente_id=cliente_id, total=total)
    db.add(orden)
    db.commit()
    db.refresh(orden)
    return orden

def generar_datos():
    db = SessionLocal()
    
    # Crear algunas categorías y proveedores
    categorias = [crear_categoria(db) for _ in range(5)]
    proveedores = [crear_proveedor(db) for _ in range(5)]
    
    # Crear clientes
    clientes = [crear_cliente(db) for _ in range(10)]
    
    # Crear productos
    for categoria in categorias:
        for proveedor in proveedores:
            for _ in range(3):  # Crear 3 productos por cada combinación de categoría y proveedor
                crear_producto(db, categoria.id, proveedor.id)
    
    # Crear órdenes
    for cliente in clientes:
        orden = crear_orden(db, cliente.id)
        # Agregar productos a la orden (relacionando productos existentes)
        productos_orden = db.query(Producto).limit(3).all()  # Selecciona 3 productos aleatorios
        for producto in productos_orden:
            cantidad = fake.random_number(digits=2)
            # Aquí se puede agregar detalles a la orden si es necesario
            db.execute(
    text(f'INSERT INTO detalles_ordenes (orden_id, producto_id, cantidad, precio) VALUES ({orden.id}, {producto.id}, {cantidad}, {producto.precio})')
)

    
    db.close()

if __name__ == '__main__':
    generar_datos()
