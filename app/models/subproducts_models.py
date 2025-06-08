from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, Field
from database import db
from typing import Optional

#Modelo para crear tabla
class SubproductTable(db.Model):
    __tablename__= "subproducts"
    
    subproduct_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    sub_name = db.Column(db.String(30), nullable=False)
    sub_description = db.Column(db.String(150), nullable=True)
    sub_stock = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            'subproduct_id': self.subproduct_id,
            'product_id': self.product_id,
            'name': self.sub_name,
            'description': self.sub_description,
            'stock': self.sub_stock
        }
    def to_public(self):
        return {
            'name': self.sub_name,
            'description': self.sub_description,
            'stock': self.sub_stock
        }


# La que todos heredan
class SubproductBase(BaseModel):
    sub_name: str = Field(min_length=3, max_length=20)
    sub_description: str = Field(min_length=5, max_length=150)

# Para mostrar publicamente
class SubproductPublic(SubproductBase):
    sub_stock: int 
    
# Para crear nuevo subproducto
class SubproductCreate(SubproductBase):
    sub_stock: int
    product_id: int 
    
# Para actualizar un subproducto
class SubproductUpdate(SubproductBase):
    sub_name: str | None = None
    sub_description: str | None = None
    sub_stock: int | None = None
    product_id: int | None = None
    
    
    

    
