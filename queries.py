# queries.py
from sqlalchemy.orm import Session
from models import Producto, Cliente, Orden, DetalleOrden
from database import SessionLocal
from sqlalchemy import text

# 1. Consultar los productos más caros
def obtener_productos_mas_caros(db: Session):
    result = db.execute(text("SELECT nombre, precio FROM productos ORDER BY precio DESC LIMIT 10"))
    
    productos = [{"nombre": row[0], "precio": row[1]} for row in result.fetchall()]
    return productos

# 2. Obtener el total de productos por categoría
def obtener_total_productos_por_categoria(db: Session):
    result = db.execute(text(""" 
        SELECT c.nombre AS categoria, COUNT(p.id) AS total_productos 
        FROM categorias c 
        JOIN productos p ON c.id = p.categoria_id 
        GROUP BY c.nombre 
    """))
    categorias = [{"categoria": row[0], "total_productos": row[1]} for row in result.fetchall()]
    return categorias

# 3. Consultar las órdenes de un cliente específico
def obtener_ordenes_por_cliente(db: Session, cliente_id: int):
    result = db.execute(text(""" 
        SELECT o.id, o.fecha, o.total 
        FROM ordenes o 
        JOIN clientes c ON o.cliente_id = c.id 
        WHERE c.id = :cliente_id 
    """), {'cliente_id': cliente_id})
    ordenes = [{"id": row[0], "fecha": row[1], "total": row[2]} for row in result.fetchall()]
    return ordenes

# 4. Obtener las órdenes con más productos
def obtener_ordenes_con_mas_productos(db: Session):
    result = db.execute(text(""" 
        SELECT o.id, COUNT(do.producto_id) AS total_productos 
        FROM ordenes o 
        JOIN detalles_ordenes do ON o.id = do.orden_id 
        GROUP BY o.id 
        ORDER BY total_productos DESC 
        LIMIT 10 
    """))
    ordenes = [{"id": row[0], "total_productos": row[1]} for row in result.fetchall()]
    return ordenes

# 5. Total de ventas por producto
def obtener_total_ventas_por_producto(db: Session):
    result = db.execute(text(""" 
        SELECT p.nombre, SUM(do.cantidad * do.precio) AS total_ventas 
        FROM productos p 
        JOIN detalles_ordenes do ON p.id = do.producto_id 
        GROUP BY p.id 
        ORDER BY total_ventas DESC 
    """))
    ventas = [{"nombre": row[0], "total_ventas": row[1]} for row in result.fetchall()]
    return ventas

# 6. Obtener los clientes con más órdenes realizadas
def obtener_clientes_con_mas_ordenes(db: Session):
    result = db.execute(text(""" 
        SELECT c.nombre, c.email, COUNT(o.id) AS total_ordenes 
        FROM clientes c 
        JOIN ordenes o ON c.id = o.cliente_id 
        GROUP BY c.id 
        ORDER BY total_ordenes DESC 
        LIMIT 10 
    """))
    clientes = [{"nombre": row[0], "email": row[1], "total_ordenes": row[2]} for row in result.fetchall()]
    return clientes

# 7. Obtener productos agotados (stock = 0)
def obtener_productos_agotados(db: Session):
    result = db.execute(text(""" 
        SELECT nombre, descripcion 
        FROM productos 
        WHERE stock = 0 
    """))
    productos_agotados = [{"nombre": row[0], "descripcion": row[1]} for row in result.fetchall()]
    return productos_agotados

# 8. Consultar la cantidad de productos vendidos por cada cliente
def obtener_cantidad_productos_vendidos_por_cliente(db: Session):
    result = db.execute(text(""" 
        SELECT c.nombre, SUM(do.cantidad) AS total_productos 
        FROM clientes c 
        JOIN ordenes o ON c.id = o.cliente_id 
        JOIN detalles_ordenes do ON o.id = do.orden_id 
        GROUP BY c.id 
        ORDER BY total_productos DESC 
    """))
    productos_vendidos = [{"nombre": row[0], "total_productos": row[1]} for row in result.fetchall()]
    return productos_vendidos

# 9. Promedio de la cantidad de productos en cada orden
def obtener_promedio_productos_por_orden(db: Session):
    result = db.execute(text(""" 
        SELECT AVG(cantidad) AS promedio_productos_por_orden 
        FROM detalles_ordenes 
    """))
    promedio = result.scalar()
    return {"promedio_productos_por_orden": promedio}

# 10. Productos vendidos por proveedor
def obtener_productos_vendidos_por_proveedor(db: Session):
    result = db.execute(text(""" 
        SELECT pr.nombre AS proveedor, 
               p.nombre AS producto, 
               COALESCE(SUM(do.cantidad), 0) AS total_vendido 
        FROM proveedores pr 
        LEFT JOIN productos p ON pr.id = p.proveedor_id 
        LEFT JOIN detalles_ordenes do ON p.id = do.producto_id 
        GROUP BY pr.nombre, p.nombre 
        ORDER BY total_vendido DESC 
    """))
    
    productos_vendidos_proveedor = [{"proveedor": row[0], "producto": row[1], "total_vendido": row[2]} for row in result.fetchall()]
    return productos_vendidos_proveedor
    
# 11. Total de ventas por orden
def obtener_total_ventas_por_orden(db: Session):
    result = db.execute(text(""" 
        SELECT o.id, o.total 
        FROM ordenes o 
        ORDER BY o.total DESC 
    """))
    ventas_ordenes = [{"id": row[0], "total": row[1]} for row in result.fetchall()]
    return ventas_ordenes

# 12. Clientes que han comprado más de un producto
def obtener_clientes_con_mas_de_un_producto(db: Session):
    result = db.execute(text(""" 
        SELECT c.nombre, c.email, COUNT(DISTINCT do.producto_id) AS productos_comprados 
        FROM clientes c 
        JOIN ordenes o ON c.id = o.cliente_id 
        JOIN detalles_ordenes do ON o.id = do.orden_id 
        GROUP BY c.id 
        HAVING productos_comprados > 1 
    """))
    clientes = [{"nombre": row[0], "email": row[1], "productos_comprados": row[2]} for row in result.fetchall()]
    return clientes

# 13. Obtener las órdenes más caras
def obtener_ordenes_mas_caras(db: Session):
    result = db.execute(text(""" 
        SELECT o.id, o.total, c.nombre AS cliente 
        FROM ordenes o 
        JOIN clientes c ON o.cliente_id = c.id 
        ORDER BY o.total DESC 
        LIMIT 10 
    """))
    ordenes_caras = [{"id": row[0], "total": row[1], "cliente": row[2]} for row in result.fetchall()]
    return ordenes_caras

# 14. Lista de productos con sus categorías
def obtener_productos_con_categorias(db: Session):
    result = db.execute(text(""" 
        SELECT p.nombre AS producto, c.nombre AS categoria 
        FROM productos p 
        JOIN categorias c ON p.categoria_id = c.id 
    """))
    productos_categorias = [{"producto": row[0], "categoria": row[1]} for row in result.fetchall()]
    return productos_categorias

# 15. Ver el historial de compras de un producto
def obtener_historial_compras_producto(db: Session, producto_id: int):
    result = db.execute(text(""" 
        SELECT o.id AS orden_id, o.fecha, do.cantidad, do.precio 
        FROM productos p 
        JOIN detalles_ordenes do ON p.id = do.producto_id 
        JOIN ordenes o ON do.orden_id = o.id 
        WHERE p.id = :producto_id 
        ORDER BY o.fecha 
    """), {'producto_id': producto_id})
    historial_compras = [{"orden_id": row[0], "fecha": row[1], "cantidad": row[2], "precio": row[3]} for row in result.fetchall()]
    return historial_compras
