from flask import Blueprint, jsonify
from database import db
from models.products_models import Product

products_bp = Blueprint("products", __name__, url_prefix="/products")

@products_bp.route('/')
def get_products():
    products = db.session.query(Product).all()  
    return jsonify([p.to_dict() for p in products])



