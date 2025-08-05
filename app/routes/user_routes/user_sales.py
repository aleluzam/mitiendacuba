from flask import Flask, Blueprint, jsonify
from app.database import db
from app.dependencies import get_id_from_jwt
from app.models.sales_models import SaleTable

user_sales_bp = Blueprint("user_sales", __name__, url_prefix=("/user"))

# Ver mi historial de compras
@user_sales_bp.route("/my_profile/my_purchases", methods = ["GET"])
def get_my_purchases():
    user_id = get_id_from_jwt()
    if not user_id:
        return jsonify({"error": "Token requerido o invalido"}), 401
    try:
        purchases = db.session.query(SaleTable).filter(SaleTable.user_id == user_id).all()
        if not purchases:
            return jsonify ({"mensaje": "Su historial de compras esta vacio"})
        return jsonify ([s.to_user() for s in purchases])
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
