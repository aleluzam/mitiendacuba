from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, Field
from database import db
from typing import Optional

# Modelo basico que heredaran todos
class ProductBase(BaseModel):
    name: str = Field(max_length=50)
    description: str = Field(max_length=300)
    price: float = Field(ge=0)

# Clase para crear la tabla de los productos
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, nullable=False)
    subproducts = db.Column(db.Boolean, default=False)    
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'stock': self.stock,
            'subproducts': self.subproducts
        }
    
# Modelo para crear un nuevo producto    
class ProductCreate(ProductBase):
    id: int 
    stock: int = Field(ge=0)
    subproducts: bool = Field(default=False)

# Modelo para mostrar producto al publico    
class ProductPublic(ProductBase):
    stock: int 

# Modelo para actualizar un producto
class ProductUpdate(ProductBase):
    name: str | None = None
    price: float | None = None
    description: str | None = None
    stock: int | None = None
    subproducts: bool | None = None
