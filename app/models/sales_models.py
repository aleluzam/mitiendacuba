from app.database import db
from pydantic import BaseModel, Field
from typing import Optional
from datetime import UTC, datetime, timezone

# TABLA VENTAS
class SaleTable(db.Model):
    __tablename__ = "sales"
    
    sale_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable = False)
    total_amount = db.Column(db.Float, nullable = False)
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    items = db.relationship("ItemsTable", backref = "sale", lazy = "joined")
    completed = db.Column(db.Boolean, default = False)
    
    def to_dict(self):
        return {
            'sale_id': self.sale_id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'created_at': self.created_at
        }
    
    def to_all(self):
        return {
            'sale_id': self.sale_id,
            'user_id': self.user_id,
            'total_amount': self.total_amount,
            'created_at': self.created_at,
            'completed': self.completed,
            'items': [p.to_dict() for p in self.items]
        }
    def to_user(self):
        return {
            'sale_id': self.sale_id,
            'total_amount': self.total_amount,
            'created_at': self.created_at,
            'completed': self.completed,
            'items': [p.to_dict() for p in self.items]
        }

    
    
    
    
### TABLA VENTA_ITEMS
class ItemsTable(db.Model):
    __tablename__ = "sale_items"
    item_id = db.Column(db.Integer, primary_key = True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sales.sale_id"), nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable = False)
    product_name = db.Column(db.String(100), nullable = False)
    product_price = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    total_amount = db.Column(db.Float, nullable = False)
    sub_name = db.Column(db.String(30), nullable = True)
    
    def to_dict(self):
        return {
            'item_id': self.item_id,
            'sale_id': self.sale_id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_price': self.product_price,
            'quantity': self.quantity,
            'total_amount': self.total_amount,
            'subproduct_name': self.sub_name
        }

    

class NewSale(BaseModel):
    user_id: int
    product_id: int
