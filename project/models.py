from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    descripcion = Column(String(255))
    precio = Column(Float)
    cantidad = Column(Integer)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    proveedor_id = Column(Integer, ForeignKey('proveedores.id'))

    categoria = relationship("Categoria", back_populates="productos")
    proveedor = relationship("Proveedor", back_populates="productos")


class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    descripcion = Column(String(255))
    
    productos = relationship("Producto", back_populates="categoria")


class Proveedor(Base):
    __tablename__ = 'proveedores'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50))
    contacto = Column(String(50))
    telefono = Column(String(15))
    
    productos = relationship("Producto", back_populates="proveedor")


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

