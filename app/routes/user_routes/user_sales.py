from flask import Blueprint, jsonify, request
from database import db
from dependencies import get_id_from_jwt
from models.sales_models import SaleTable

user_sales_bp = Blueprint("user_sales", __name__, url_prefix = ("/user"))

# VER MI HISTORIAL DE COMPRAS
@user_sales_bp.route("/my_profile/my_purchases", methods = ["GET"])
def get_my_sales():
    user_id = get_id_from_jwt()
    if not user_id:
        return jsonify ({"error": "Token invalido o requerido"}), 401
    try:
        sales = db.session.query(SaleTable).filter(SaleTable.user_id == user_id).all()
        if not sales:
            return jsonify ({"mensaje": "Historial de compras vacio"})
        return jsonify ([s.to_user() for s in sales])
    
    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500

    