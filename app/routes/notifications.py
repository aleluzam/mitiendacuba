from models.notifications_models import NotificationUserTable, NotificationTable
from flask import request, jsonify, Blueprint
from database import db
from dependencies import get_id_from_jwt
from models.users_models import UserTable
notifications_bp = Blueprint("notifications", __name__)



# VER TODAS LAS NOTIFICACIONES (ADMIN)
@notifications_bp.route("/admin/all_notifications", methods = ["GET"])
def all_notifications():
    try:
        notifications = db.session.query(NotificationTable).all()
        return jsonify ([n.to_admin() for n in notifications])
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500



# VER TODAS LAS NOTIFICACIONES POR USUARIO (ADMIN)
@notifications_bp.route("/admin/all_users_notifications", methods = ["GET"])
def all_users_notifications():
    try:
        users_notifications = db.session.query(NotificationUserTable).all()
        return jsonify ([n.to_admin() for n in users_notifications])
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500



# VER MIS NOTIFICACIONES (USER)
@notifications_bp.route("/user/my_profile/my_notifications", methods = ["GET"])
def get_my_notifications():
    user_id = get_id_from_jwt()
    if not user_id:
        return jsonify ({"error": "Token requerido o invalido"}), 401
    try:
        my_notifications = db.session.query(NotificationUserTable).filter(NotificationUserTable.user_id == user_id).all()
        if not my_notifications:
            return jsonify ({"message": "Usted no tiene nuevas notificaciones"})
        
        return jsonify ([n.to_user() for n in my_notifications])
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500



@notifications_bp.route("/admin/create_notification", methods=["POST"])
def create_new_notification():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Datos requeridos"}), 400
    
    title = data.get("title")
    if not title or not title.strip():
        return jsonify({"error": "Titulo de notificacion requerido"}), 400
    message = data.get("message")
    if not message or not message.strip():
        return jsonify({"error": "Mensaje de notificacion requerido"}), 400
    
    users_id = data.get("users_id")
    if users_id is None:
        users = db.session.query(UserTable).all()
        users_id = [u.user_id for u in users]
    if not users_id:
        return jsonify ({"error": "No hay usuarios registrados"}), 400
    try:
        new_notification = NotificationTable(
            title = title,
            message = message
        )
        db.session.add(new_notification)
        db.session.flush()
        
        for u in users_id:
            new_user_notification = NotificationUserTable(
                notification_id = new_notification.notification_id,
                user_id = u
            )
            db.session.add(new_user_notification)
        db.session.commit()
        return jsonify ({"message": "Notificacion creada exitosamente"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
            