from pydantic import BaseModel, Field, ConfigDict
from app.database import db
from typing import Optional


# Clase para crear la tabla de los productos
class ProductTable(db.Model):
    __tablename__ = 'products'
    
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    stock = db.Column(db.Integer, nullable=False)
    subproducts = db.Column(db.Boolean, default=False)    
    limit_stock = db.Column(db.Integer, nullable = False)
    featured = db.Column(db.Boolean, default = False)
    img_url = db.Column(db.String(150))
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"), nullable = False)

    subproducts_list = db.relationship("SubproductTable", backref = "product", lazy = "joined")
    section = db.relationship("SectionTable", lazy = "joined", backref = "product")
    
    
    def to_dict(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'stock': self.stock,
            'subproducts': self.subproducts,
            'limit_stock': self.limit_stock,
            'featured': self.featured,
            'section': self.section.get_name() if self.section else None,
            'img_url': self.img_url 
        }
    
    def to_public(self):
        return {
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'stock': self.stock,
            'section': self.section.get_name() if self.section else None,
            'featured': self.featured,
            'img_url': self.img_url 

        }
    
    def to_all(self):
        return {
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'stock': self.stock, 
            'section': self.section.get_name() if self.section else None,
            'featured': self.featured,
            'product_id': self.product_id,
            'img_url': self.img_url,
            'subproducts_list': [p.to_public() for p in self.subproducts_list] if self.subproducts_list else None
        }



    # Modelo basico que heredan todos
class ProductBase(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(max_length=300)
    price: float = Field(ge=0)
    img_url: str | None = None

        
# Modelo para crear un nuevo producto    
class ProductCreate(ProductBase):
    stock: int = Field(ge=0)
    subproducts: bool = Field(default=False)
    section_id: int
    
    model_config = ConfigDict(from_attributes=True)


# Modelo para mostrar producto al publico    
class ProductPublic(ProductBase):
    stock: int 
    subproducts: bool = Field(default=False)



# Modelo para actualizar un producto
class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=50)
    price: float | None = Field(None, ge=0)
    description: str | None = Field(None, max_length=300)
    stock: int | None = Field(None, ge=0)
    subproducts: bool | None = None
    section_id: int | None = None
    
    
