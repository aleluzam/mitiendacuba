from flask import request, jsonify, Blueprint
from models.users_models import UserUpdate, UserTable

user_users_bp = Blueprint("user_users", __name__, url_prefix=("/user"))



# EDITAR USUARIO
@user_users_bp.route("/")
def user_edit():
    