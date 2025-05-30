from flask import Blueprint, request, jsonify
from database import db
from security import verify_credentials
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

auth_bp = Blueprint("authentication", __name__, url_prefix="/login")


@auth_bp.route("/", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Username y contraseña requeridos"}), 400
        
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return jsonify({"error": "Username y contraseña requeridos"}), 400
        
        # Aquí ya puedes trabajar con el resultado como diccionario
        verification_result = verify_credentials(username, password)
        
        if verification_result["valid"]:
            user = verification_result["user"]
            
            payload = {
                "user_id": user.user_id,
                "username": user.username,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            #if user.role == "admin":
                #redirect_url = "/admin"
            #if user.role == "client":
                #redirect_url = "/user"
            return jsonify({
                "message": "Login exitoso",
                "token": token,
                "user": {
                    "id": user.user_id,
                    "username": user.username
                    #"role": user.role
                }
            })
        else:
            return jsonify(verification_result), 401
                   
    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
        
    
    