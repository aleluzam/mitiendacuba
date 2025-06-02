from flask import Blueprint, jsonify, request
from database import db
from models.users_models import UserCreate, User, UserTable
from datetime import datetime, UTC
from security import login_required

admin_users_bp = Blueprint("users", __name__, url_prefix="/admin")



# Mostrar todos los usuarios existentes
@admin_users_bp.route("/all_users")
@login_required
def get_all_users():
    users = db.session.query(UserTable).all()
    return jsonify([p.to_dict() for p in users])

#Obtener usaurio por id (para admin)
@admin_users_bp.route("/user/<data_id>", methods=["GET"])
def get_user(data_id):
    user = db.session.query(UserTable).filter(UserTable.user_id == data_id ).first()
    if not user:
        return jsonify({"error": "ID incorrecta"}), 400
    else: 
        return jsonify(user.to_dict())

# Eliminar usuario por id (para admin)
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


