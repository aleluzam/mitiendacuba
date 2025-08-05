from flask import Blueprint, jsonify, request
from app.database import db
from app.models.users_models import UserCreate, User, UserTable
from datetime import datetime, UTC
from app.security import login_required, admin_only

admin_users_bp = Blueprint("admin_users", __name__, url_prefix="/admin")



# MOSTRAR TODOS LOS USUARIOS (ADMIN)
@admin_users_bp.route("/all_users")
def get_all_users():
    users = db.session.query(UserTable).all()
    if not users:
        return jsonify({"message": "No hay usuarios registrados"})
    try:
        return jsonify([p.to_dict() for p in users])
    
    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500

    



# OBTENER USUARIO POR ID (ADMIN)
@admin_users_bp.route("/user/<data_id>", methods=["GET"])
def get_user(data_id):
    user = db.session.query(UserTable).filter(UserTable.user_id == data_id ).first()
    if not user:
        return jsonify({"error": "ID incorrecta"}), 400
    else: 
        return jsonify(user.to_dict())
    
    

# ELIMINAR USUARIO POR ID (ADMIN)
@admin_users_bp.route("/user/delete/<data_id>", methods=["DELETE"])
def delete_user(data_id):
    verify_id = db.session.query(UserTable).filter(UserTable.user_id == data_id ).first()
    if not verify_id:
        return jsonify({"error": "ID incorrecta"}), 400
    else: 
        try:
            db.session.delete(verify_id)
            db.session.commit()
            return jsonify({"mensaje": f"El usaurio de id {data_id} ha sido eliminado correctamente"})
        except:
            db.session.rollback()
            return jsonify({"error": f"Error al eliminar el usaurio de id {data_id}"}), 500


