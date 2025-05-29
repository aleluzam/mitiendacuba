from flask import Blueprint, jsonify, request
from database import db
from models.users import UserCreate, User, UserTable
from datetime import datetime, UTC

users_admin_bp = Blueprint("users", __name__, url_prefix="/admin")

@users_admin_bp.route("/all_users")
def get_all_users():
    users = db.session.query(UserTable).all()
    return jsonify([p.to_dict() for p in users])

