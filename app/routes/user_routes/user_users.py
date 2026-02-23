from flask import request, jsonify, Blueprint
from models.users_models import UserUpdate, UserTable, UserNewPassword
from dependencies import get_id_from_jwt
from database import db
from pydantic import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from security import user_only


user_users_bp = Blueprint("user_users", __name__, url_prefix=("/user"))



# VER MI PERFIL DE USUARIO
@user_users_bp.route("/my_profile", methods = ["GET"])
def my_profile():
    user_id = get_id_from_jwt()
    if not user_id:
        return jsonify ({"error": "Token requerido o invalido"}), 401
    try:
        user_profile = db.session.query(UserTable).filter(UserTable.user_id == user_id).first()
        if not user_profile:
            return jsonify ({"error": "Usuario no encontrado"}), 404
        return jsonify (user_profile.to_public())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
        
        
       
# EDITAR MI PERFIL DE USUARIO
@user_users_bp.route("/my_profile/edit", methods = ["PUT", "PATCH"])
def edit_profile():
    user_id = get_id_from_jwt()
    if not user_id: 
        return jsonify ({"error": "Token requerido o invalido"}), 401 # Unauthorized
    try:
        data = UserUpdate.model_validate(request.get_json())
        to_edit = db.session.query(UserTable).filter(UserTable.user_id == user_id).first()
        if not to_edit:
            return jsonify ({"error": "Usuario no encontrado"}), 404
        
        validate_data = data.model_dump(exclude_unset=True)
        if "username" in validate_data:
            verify_username = db.session.query(UserTable).filter(UserTable.username == validate_data["username"], UserTable.user_id != user_id).first()
            if verify_username:
                return jsonify ({"error": "El nombre de usuario ya existe"}), 409

        
        for field, value in validate_data.items():
            setattr(to_edit, field, value)
        db.session.commit()
        return jsonify ({"mensaje": "Perfil actualizado",
                         "Perfil": {
                             "username": to_edit.username,
                             "name": to_edit.name,
                             "last_name": to_edit.last_name,
                             "mobile": to_edit.mobile,
                             "mail": to_edit.mail
                         }})
    except ValidationError as e:
        return jsonify({
            "error": "Datos inválidos",
            "details": [{"field": err['loc'][0], "message": err['msg']} 
                       for err in e.errors()]
        }), 400 
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
        
        
        
# ELIMINAR MI PERFIL
@user_users_bp.route("/my_profile/delete", methods = ["DELETE"])
def delete_user():
    user_id = get_id_from_jwt()
    if not user_id:
        return jsonify ({"error": "Token requerido o invalido"}), 401
    
    try:
        user = db.session.query(UserTable).filter(UserTable.user_id == user_id).first()
        if not user: 
            return jsonify ({"error": "Usuario no encontrado"}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify ({"mensaje": "Su perfil fue eliminado correctamente",
                         "logout": True}) # avisa al fronted que se acabo el log
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500

                    
# RESTABLECER CONTRASEÑA DE MI PERFIL
@user_users_bp.route("/my_profile/change_password", methods = ["PUT", "PATCH"])
def change_password():
    
    user_id = get_id_from_jwt()
    if not user_id:
        return jsonify ({"error": "Token requerido o invalido"}), 401
    
    data = request.get_json()
    if not data:
        return jsonify ({"error": "Datos requeridos"}), 400
    actual_password = data["actual_password"]
    if not actual_password:
        return jsonify ({"error": "Contraseña actual requerida"}), 400
    new_password = data["new_password"]
    if not new_password:
        return jsonify ({"error": "Nueva contraseña requerida"}), 400
    
    try:
        user = db.session.query(UserTable).filter(UserTable.user_id == user_id).first()
        if not user:
            return jsonify ({"error": "Usuario no encontrado"}), 404
        verify_password = check_password_hash(user.password_hash, actual_password)
        if not verify_password:
            return jsonify ({"error": "Contraseña actual incorrecta"}), 400
        
        new_password_hash = generate_password_hash(new_password)
        user.password_hash = new_password_hash
        db.session.commit()
        return jsonify ({"message": "Contraseña cambiada con exito",
                         "logout": True}) # avisa al front que tiene que cerrar sesion
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Error interno del servidor",
            "details": str(e)
        }), 500
    
    

