from flask import request, jsonify, Blueprint
from database import db
from models.products_models import ProductPublic, ProductTable
from pydantic import ValidationError

user_products_bp = Blueprint("user_products", __name__, url_prefix="/user")

### PRODUCTOS ###

# MOSTRAR PRODUCTOS CON RESPECTIVOS SUBPRODUCTOS
@user_products_bp.route("/all_products", methods = ["GET"])
def get_all():
    try:
        data = db.session.query(ProductTable).all()
        return jsonify ([p.to_all() for p in data])
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500

# VER UN PRODUCTO CON SUBPRODUCTOS
@user_products_bp.route("/product/<product_id>", methods = ["GET"])
def get_product(product_id):
    product = db.session.query(ProductTable).filter(ProductTable.product_id == product_id).first()
    if not product:
        return jsonify ({"error": "Producto no encontrado"}), 404
    try:
        return jsonify(product.to_all())
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500





