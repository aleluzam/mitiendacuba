from database import db
from datetime import datetime, timezone, timedelta


class CodeTable(db.Model):
    __tablename__ = 'codes'
    
    code_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    code = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime, nullable = False, default = lambda: datetime.now(timezone.utc) + timedelta(minutes=15))
    used = db.Column(db.Boolean, nullable = False, default = False)
    
    def to_admin(self):
        return{
            'code_id': self.code_id,
            'user_id': self.user_id,
            'code': self.code,
            'created_at': self.created_at,
            'expires_at': self.expires_at,
            'used': self.used
        }