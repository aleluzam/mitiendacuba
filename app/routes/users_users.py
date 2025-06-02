from flask import jsonify, request, Blueprint
from database import db
from models.users_models import UserTable
from werkzeug.security import generate_password_hash
from models.users_models import User


user_bp = Blueprint("user_public", __name__, url_prefix="/user")



