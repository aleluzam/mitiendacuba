from flask import Blueprint, request, jsonify
from database import db
from security import verify_credentials
import jwt
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from models.users_models import UserTable

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

auth_bp = Blueprint("authentication", __name__, url_prefix="/auth")


# REGISTRARSE. crear nuevo usuario
@auth_bp.route("/register", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": " No se enviaron los datos"}), 400
        
        required_fields = ['username', 'name', 'last_name', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'El campo {field} es requerido'}), 400
        
        existing_user = db.session.query(UserTable).filter(
            UserTable.username == data['username']
        ).first()
        
        if existing_user:
            return jsonify({'error': 'El username ya existe'}), 409
        
        if len(data['password']) < 8:
            return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres'}), 400
        password_hash = generate_password_hash(data['password'])
        
        new_user = UserTable(
            username=data['username'].lower().strip(),
            password_hash=password_hash,
            name=data['name'].strip().title(),
            last_name=data['last_name'].strip().title(),
            mobile=data.get('mobile'), 
            is_active=True
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'user': {
                'user_id': new_user.user_id,
                'username': new_user.username,
                'name': new_user.name,
                'last_name': new_user.last_name,
                'mobile': new_user.mobile,
                'created_at': new_user.created_at.isoformat(),
                'is_active': new_user.is_active
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error interno del servidor: {str(e)}'}), 500



# Iniciar sesion
@auth_bp.route("/login", methods=["POST"])
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
        
    
    