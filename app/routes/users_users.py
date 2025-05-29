from flask import jsonify, request, Blueprint
from database import db
from models.users import UserTable
from werkzeug.security import generate_password_hash
from models.users import User


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




# Crear un nuevo usuario
@user_bp.route("/create", methods=["POST"])
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
    
