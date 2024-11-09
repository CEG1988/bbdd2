from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Cliente, Categoria, Proveedor, Producto, Orden
from database import SessionLocal  
from queries import (
    contar_productos,
    listar_productos_sin_stock,
    listar_clientes,
    contar_categorias,
    listar_proveedores,
    producto_mas_caro,
    producto_mas_barato,
    contar_ordenes,
    listar_ordenes_con_cliente,
    detalles_ordenes_cliente,
    total_vendido,
    contar_productos_por_categoria,
    promedio_precio_por_categoria,
    contar_ordenes_por_cliente,
    listar_productos_y_proveedor
)

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
            for _ in range(3):  
                crear_producto(db, categoria.id, proveedor.id)
    
    # Crear órdenes
    for cliente in clientes:
        orden = crear_orden(db, cliente.id)
        
        productos_orden = db.query(Producto).limit(3).all() 
        for producto in productos_orden:
            cantidad = fake.random_number(digits=2)
            
            db.execute(
    text(f'INSERT INTO detalles_ordenes (orden_id, producto_id, cantidad, precio) VALUES ({orden.id}, {producto.id}, {cantidad}, {producto.precio})')
)

if __name__ == '__main__':
    generar_datos()

# Función para ejecutar todas las consultas
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from consultas import (
    obtener_productos_mas_caros,
    obtener_total_productos_por_categoria,
    obtener_ordenes_por_cliente,
    obtener_ordenes_con_mas_productos,
    obtener_total_ventas_por_producto,
    obtener_clientes_con_mas_ordenes,
    obtener_productos_agotados,
    obtener_cantidad_productos_vendidos_por_cliente,
    obtener_promedio_productos_por_orden,
    obtener_productos_vendidos_por_proveedor,
    obtener_total_ventas_por_orden,
    obtener_clientes_con_mas_de_un_producto,
    obtener_ordenes_mas_caras,
    obtener_productos_con_categorias,
    obtener_historial_compras_producto
)

# Función para obtener una sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para ejecutar todas las consultas
def ejecutar_consultas():
    
    db = next(get_db())

    print("Ejecutando consultas...")

    # Ejecuta todas las consultas
    productos_mas_caros = obtener_productos_mas_caros(db)
    print("Productos más caros:", productos_mas_caros)

    total_productos_categoria = obtener_total_productos_por_categoria(db)
    print("Total productos por categoría:", total_productos_categoria)

    ordenes_cliente = obtener_ordenes_por_cliente(db, 2)  
    print("Órdenes del cliente 1:", ordenes_cliente)

    ordenes_con_mas_productos = obtener_ordenes_con_mas_productos(db)
    print("Órdenes con más productos:", ordenes_con_mas_productos)

    total_ventas_producto = obtener_total_ventas_por_producto(db)
    print("Ventas por producto:", total_ventas_producto)

    clientes_con_mas_ordenes = obtener_clientes_con_mas_ordenes(db)
    print("Clientes con más órdenes:", clientes_con_mas_ordenes)

    productos_agotados = obtener_productos_agotados(db)
    print("Productos agotados:", productos_agotados)

    cantidad_productos_cliente = obtener_cantidad_productos_vendidos_por_cliente(db)
    print("Cantidad de productos vendidos por cliente:", cantidad_productos_cliente)

    promedio_productos_por_orden = obtener_promedio_productos_por_orden(db)
    print("Promedio de productos por orden:", promedio_productos_por_orden)

    productos_vendidos_proveedor = obtener_productos_vendidos_por_proveedor(db)
    print("Productos vendidos por proveedor:", productos_vendidos_proveedor)

    total_ventas_por_orden = obtener_total_ventas_por_orden(db)
    print("Ventas por orden:", total_ventas_por_orden)

    clientes_con_mas_producto = obtener_clientes_con_mas_de_un_producto(db)
    print("Clientes que han comprado más de un producto:", clientes_con_mas_producto)

    ordenes_mas_caras = obtener_ordenes_mas_caras(db)
    print("Órdenes más caras:", ordenes_mas_caras)

    productos_con_categorias = obtener_productos_con_categorias(db)
    print("Productos con sus categorías:", productos_con_categorias)

    historial_compras_producto = obtener_historial_compras_producto(db, 4)  
    print("Historial de compras del producto 1:", historial_compras_producto)

    # Cierra la sesión de la base de datos
    db.close()

# Función principal
if __name__ == "__main__":
    
    ejecutar_consultas()
