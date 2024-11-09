from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from database import SessionLocal, engine
from models import Base
from queries import (
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

# Inicializar la base de datos y la aplicación FastAPI
Base.metadata.create_all(bind=engine)
app = FastAPI()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Monta la carpeta static para servir archivos como CSS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configura Jinja2Templates para manejar las plantillas HTML
templates = Jinja2Templates(directory="templates")

# Dependencia para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para mostrar la interfaz de consulta en HTML
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta de consulta
@app.get("/consulta/{tipo}")
async def consulta(tipo: str, db: Session = Depends(get_db)):
    try:
        if tipo == 'productos_caros':
            result = obtener_productos_mas_caros(db)
        elif tipo == 'productos_por_categoria':
            result = obtener_total_productos_por_categoria(db)
        elif tipo == 'ordenes_cliente':
            result = obtener_ordenes_por_cliente(db, cliente_id=1)
        elif tipo == 'ordenes_mas_productos':
            result = obtener_ordenes_con_mas_productos(db)
        elif tipo == 'ventas_producto':
            result = obtener_total_ventas_por_producto(db)
        elif tipo == 'clientes_con_mas_ordenes':
            result = obtener_clientes_con_mas_ordenes(db)
        elif tipo == 'productos_agotados':
            result = obtener_productos_agotados(db)
        elif tipo == 'productos_vendidos_cliente':
            result = obtener_cantidad_productos_vendidos_por_cliente(db)
        elif tipo == 'promedio_productos_orden':
            result = obtener_promedio_productos_por_orden(db)
        elif tipo == 'productos_vendidos_proveedor':
            result = obtener_productos_vendidos_por_proveedor(db)
        elif tipo == 'ventas_por_orden':
            result = obtener_total_ventas_por_orden(db)
        elif tipo == 'clientes_mas_de_un_producto':
            result = obtener_clientes_con_mas_de_un_producto(db)
        elif tipo == 'ordenes_mas_caras':
            result = obtener_ordenes_mas_caras(db)
        elif tipo == 'productos_con_categorias':
            result = obtener_productos_con_categorias(db)
        elif tipo == 'historial_compras_producto':
            result = obtener_historial_compras_producto(db, producto_id=1)
        else:
            raise HTTPException(status_code=400, detail="Consulta no válida")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


