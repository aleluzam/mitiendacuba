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
    
    
    
# MOSTRAR UN PRODUCTO POR ID (USER)
@user_products_bp.route("/product/<product_id>", methods = ["GET"])    
def get_product(product_id):
    try:
        product = db.session.query(ProductTable).filter(ProductTable.product_id == product_id).first()
        if not product:
            return jsonify ({"mensaje": f"No existe producto de id {product_id}"}), 404
        return jsonify (product.to_public())
  
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500

    