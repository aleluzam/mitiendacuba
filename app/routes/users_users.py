from flask import jsonify, request, Blueprint
from database import db
from models.users_models import UserTable
from werkzeug.security import generate_password_hash
from models.users_models import User


user_bp = Blueprint("user_public", __name__, url_prefix="/user")

#Obtener usaurio por id
@user_bp.route("/<data_id>", methods=["GET"])
def get_user(data_id):
    verify_id = db.session.query(UserTable).filter(UserTable.user_id == data_id ).first()
    if not verify_id:
        return jsonify({"error": "ID incorrecta"}), 400
    else: 
        user_public = User.model_validate(verify_id)
        return jsonify(user_public.model_dump())


# Borrar un usuario
@user_bp.route("/delete/<data_id>", methods=["DELETE"])
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
    
