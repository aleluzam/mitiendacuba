from flask import request, jsonify, Blueprint
from database import db
from models.products_models import ProductPublic, ProductTable
from pydantic import ValidationError

user_products_bp = Blueprint("user_products", __name__, url_prefix="/user")

# VER TODOS LOS PRODUCTOS
@user_products_bp.route("/all_products")
def get_all_products():
    try:
        products = db.session.query(ProductTable).all()
        return jsonify ([p.to_public() for p in products])
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
    