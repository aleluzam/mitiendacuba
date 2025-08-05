from app.database import db
from datetime import datetime, timezone


class NotificationTable(db.Model):
    __tablename__ = 'notifications'
    
    notification_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    message = db.Column(db.String(500), nullable = False)
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    
    def to_admin(self):
        return {
            
            'notification_id': self.notification_id,
            'title': self.title,
            'message': self.message,
            'created_at': self.created_at
        }
    
    def to_user(self):
        return {
            'title': self.title,
            'message': self.message,
            'created_at': self.created_at
        }
    
class NotificationUserTable(db.Model):
    __tablename__ = 'notifications_users'
    
    id = db.Column(db.Integer, primary_key = True)
    notification_id = db.Column(db.Integer, db.ForeignKey("notifications.notification_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    is_read = db.Column(db.Boolean, nullable = False, default = False)
    notification_details = db.relationship("NotificationTable", backref = "user_notification", lazy = "joined")
    
    def to_admin(self): 
        return {
            'user_id': self.user_id,
            'is_read': self.is_read,
            'notification_details': self.notification_details.to_admin() if self.notification_details else None
        }

    def to_user(self):
        return {
            'notification': self.notification_details.to_user() if self.notification_details else None
        }
