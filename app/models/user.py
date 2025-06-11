from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from enum import Enum

class Role(Enum):
    READER = 'reader'
    AUTHOR = 'author'
    ADMIN = 'admin'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(Role), default=Role.READER)
    avatar_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    social_links = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == Role.ADMIN

    bookmarks = db.relationship('Bookmark', back_populates='user', lazy='dynamic')
    view_logs = db.relationship('ViewLog', back_populates='user', lazy='dynamic')
    notifications = db.relationship('Notification', back_populates='user', lazy='dynamic')