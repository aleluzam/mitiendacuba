from flask import Flask, jsonify, Blueprint
from database import db
from models.notifications_models import NotificationTable

admin_notifications_bp = Blueprint("notifications", __name__, url_prefix=("/admin"))

@admin_notifications_bp.route("/all_notifications", methods = ["GET"])
def all_notifications():
    notifications = db.session.query(NotificationTable).all()
    return jsonify ([p.to_admin() for p in notifications])



