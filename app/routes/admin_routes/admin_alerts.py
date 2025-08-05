from flask import Flask, jsonify, Blueprint
from app.database import db
from app.models.alerts_models import AlertTable
from app.models.products_models import ProductTable
from zoneinfo import ZoneInfo
from datetime import datetime

cuba_tz = ZoneInfo('America/Havana')

admin_alerts_bp = Blueprint("alerts", __name__, url_prefix=("/admin"))

# VER TODAS LAS ALERTAS
@admin_alerts_bp.route("/all_alerts", methods = ["GET"])
def all_alerts():
    alerts = db.session.query(AlertTable).all()
    return jsonify ([p.to_admin() for p in alerts])

# CREAR UNA ALERTA POR STOCK LIMITE
def stock_alerts(product_id):
    try:
        product = db.session.query(ProductTable).filter(ProductTable.product_id == product_id).first()
        if product.stock <= product.limit_stock:
            validate_alert = db.session.query(AlertTable).filter(AlertTable.product_id == product_id).first()
            if not validate_alert:
                
                new_alert = AlertTable(
                    product_id = product.product_id,
                    product_name = product.name,
                    message = "Baja cantidad de stock del producto",
                    actual_stock = product.stock,
                    limit_stock = product.limit_stock,
                    created_at = datetime.now(cuba_tz),
                )
                db.session.add(new_alert)
                db.session.commit()
            else:
                validate_alert.actual_stock = product.stock
                db.session.commit()
                
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
