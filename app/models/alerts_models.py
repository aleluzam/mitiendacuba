from flask import Flask
from pydantic import BaseModel
from app.database import db
from datetime import datetime, timezone


class AlertTable(db.Model):
    __tablename__ = "alerts"
    
    id = db.Column(db.Integer, primary_key = True)
    product_id = db.Column(db.Integer, nullable = False)
    product_name = db.Column(db.String(30), nullable = False)
    message = db.Column(db.String(100), nullable = False)
    actual_stock = db.Column(db.Integer, nullable = False)
    limit_stock = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    
    def to_admin(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'message': self.message,
            'actual_stock': self.actual_stock,
            'limit_stock': self.limit_stock,
            'created_at': self.created_at
        }
    
    
    
    

    
    
    
