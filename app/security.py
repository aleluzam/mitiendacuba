from flask import request, jsonify
from database import db
from models.users_models import UserTable
from werkzeug.security import check_password_hash
from functools import wraps
import jwt
import os
from dotenv import load_dotenv

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
        
