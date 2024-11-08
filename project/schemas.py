from pydantic import BaseModel
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    cantidad: int

class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    cantidad: int
    class Config:
        orm_mode = True

class ClienteCreate(BaseModel):
    nombre: str
    email: str

class Cliente(BaseModel):
    id: int
    nombre: str
    email: str
    class Config:
        orm_mode = True

class OrdenCreate(BaseModel):
    cliente_id: int
    total: float

class Orden(BaseModel):
    id: int
    cliente_id: int
    total: float
    class Config:
        orm_mode = True
