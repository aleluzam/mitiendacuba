from flask import Blueprint, jsonify, request
from database import db
from models.users import UserCreate, User, UserTable
from werkzeug.security import generate_password_hash
from datetime import datetime, UTC

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/")
def get_all_users():
    users = db.session.query(UserTable).all()
    return jsonify([p.to_dict() for p in users])

@users_bp.route("/create", methods=["POST"])
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