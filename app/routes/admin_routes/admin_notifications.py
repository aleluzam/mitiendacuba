from flask import Flask, jsonify, Blueprint
from database import db
from models.notifications_models import NotificationTable
<<<<<<< HEAD
from models.products_models import ProductTable
from zoneinfo import ZoneInfo
from datetime import datetime

cuba_tz = ZoneInfo('America/Havana')

admin_notifications_bp = Blueprint("notifications", __name__, url_prefix=("/admin"))


# VER TODAS LAS NOTIFICACIONES
=======

admin_notifications_bp = Blueprint("notifications", __name__, url_prefix=("/admin"))

>>>>>>> c037a7696cf69cd473c9a034f71011fc11f43ed0
@admin_notifications_bp.route("/all_notifications", methods = ["GET"])
def all_notifications():
    notifications = db.session.query(NotificationTable).all()
    return jsonify ([p.to_admin() for p in notifications])


<<<<<<< HEAD
# CREAR UNA NOTIFICACION POR STOCK LIMITE
def stock_notification(product_id):
    try:
        product = db.session.query(ProductTable).filter(ProductTable.product_id == product_id).first()
        if product.stock <= product.limit_stock:
            validate_notification = db.session.query(NotificationTable).filter(NotificationTable.product_id == product_id).first()
            if not validate_notification:
                
                new_notification = NotificationTable(
                    product_id = product.product_id,
                    product_name = product.name,
                    message = "Baja cantidad de stock del producto",
                    actual_stock = product.stock,
                    limit_stock = product.limit_stock,
                    created_at = datetime.now(cuba_tz),
                )
                db.session.add(new_notification)
                db.session.commit()
            else:
                validate_notification.actual_stock = product.stock
                db.session.commit()
                
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500

    
    
    
    



=======
>>>>>>> c037a7696cf69cd473c9a034f71011fc11f43ed0

