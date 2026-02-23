from flask import request, jsonify
from database import db
from models.users_models import UserTable
from werkzeug.security import check_password_hash
from functools import wraps
import jwt
import os
from dotenv import load_dotenv
from dependencies import get_id_from_jwt

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def verify_credentials(username, password):
    """Función pura que solo verifica credenciales"""
    try:
        user = db.session.query(UserTable).filter(UserTable.username == username).first()
        if user and check_password_hash(user.password_hash, password):
            return {"valid": True, "user": user}
        else:
            return {"valid": False, "error": "Credenciales inválidas"}
    except Exception as e:
        return {"valid": False, "error": f"Error interno: {str(e)}"}


# Funcion para generar decorador verificar de token
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs): 
        token = None
        
        if "Authorization" not in request.headers:
            return jsonify({"message": "Token requerido"}), 401
            
        auth_header = request.headers["Authorization"]
        
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"message": "Formato de token incorrecto"}), 401
            
        if not token:
            return jsonify({"message": "Token requerido"}), 401
            
        try: 
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data["username"]
            #user_role = data["role"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expirado"}), 401
        #except jwt.InvalidTokenError:
            #return jsonify({"message": "Token invalido"}), 401  #           
        return f(*args, **kwargs) 
    return decorated 



# DECORADOR PARA SOLO ADMINS
def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = get_id_from_jwt()
        if not user_id:
            return jsonify ({"error": "Token invalido o requerido"}), 401
        try:
            user = db.session.query(UserTable).filter(UserTable.user_id == user_id).first()
            if not user:
                return jsonify ({"error": "Usuario no encontrado"}), 404
            if user.role != "admin":
                return jsonify ({"error": "Acceso denegado. Solo para admins"}), 403 # FORBIDDEN prohibido
            
            return f(*args, **kwargs)
        
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    return decorated



# DECORADOR PARA SOLO USERS
def user_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = get_id_from_jwt()
        if not user_id:
            return jsonify ({"error": "Token invalido o requerido"}), 401
        try:
            user = db.session.query(UserTable).filter(UserTable.user_id == user_id).first()
            if not user:
                return jsonify ({"error": "Usuario no encontrado"}), 404
            if user.role != "user":
                return jsonify ({"error": "Acceso denegado. Solo para users"}), 403 # FORBIDDEN prohibido
            
            return f(*args, **kwargs)
        
        except Exception as e:
            return jsonify({"error": f"Error interno: {str(e)}"}), 500
    return decorated
    
    
                
        

        
