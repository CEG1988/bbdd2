# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:Huawei1234@127.0.0.1:3306/tiendas"

# Crea el engine para la base de datos
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})

# Crea una clase base para los modelos
Base = declarative_base()

# Configura la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    descripcion = Column(String(255))
    precio = Column(Float)
    cantidad = Column(Integer)

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)

class Orden(Base):
    __tablename__ = 'ordenes'
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    total = Column(Float)
    cliente = relationship("Cliente")

class DetalleOrden(Base):
    __tablename__ = 'detalles_ordenes'
    id = Column(Integer, primary_key=True, index=True)
    orden_id = Column(Integer, ForeignKey('ordenes.id'))
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer)
    precio = Column(Float)
    
    orden = relationship("Orden", back_populates="detalles")
    producto = relationship("Producto")

# Relación inversa en Orden
Orden.detalles = relationship("DetalleOrden", back_populates="orden")
