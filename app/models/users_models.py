from flask_sqlalchemy import SQLAlchemy 
from pydantic import BaseModel, Field, ConfigDict
from database import db
from typing import Optional
from datetime import datetime, timezone

# MODELO SQLALCHEMY
class UserTable(db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False, unique=True)  
    password_hash = db.Column(db.String(255), nullable=False)  
    name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    mobile = db.Column(db.String(15), nullable=True)  
    is_active = db.Column(db.Boolean, default=True, nullable=False)  
    mail = db.Column(db.String(120), unique = True, nullable = False)
    

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'name': self.name,
            'last_name': self.last_name,
            'mobile': self.mobile,
            'is_active': self.is_active,
            'mail': self.mail
        }
        
    def to_public(self):
        return {
            'username': self.username,
            'name': self.name,
            'last_name': self.last_name,
            'mobile': self.mobile,
            'mail': self.mail
        }

    def __repr__(self):
        return f'<User {self.username}>'


class User(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    name: str = Field(min_length=2, max_length=15)
    last_name: str = Field(min_length=2, max_length=15)
    mobile: str | None = Field(max_length=15, default=None)
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=15)
    name: str = Field(min_length=2, max_length=15)
    last_name: str = Field(min_length=2, max_length=15)
    mobile: str | None = Field(max_length=15, default=None)  
    password: str = Field(min_length=8, max_length=128)
    mail: str = Field(min_length=10, max_length=120)
    
    model_config = ConfigDict(from_attributes=True)
    

class UserUpdate(BaseModel):
    username: str | None = Field(min_length=3, max_length=15, default=None)
    name: str | None = Field(min_length=2, max_length=15, default=None)
    last_name: str | None = Field(min_length=2, max_length=15, default=None)
    mobile: str | None = Field(max_length=15, default=None)
    mail: str | None = Field(max_length=120, default= None)
    
    
    

class Users(User):
    user_id: int
    created_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)
    
    
    
class UserNewPassword(BaseModel):
    new_password: str = Field(min_length=8, max_length=128)
    mobile: str | None = Field(max_length=15, default=None)




