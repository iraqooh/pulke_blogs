from app import db
from datetime import datetime

class ViewLog(db.Model):
    __tablename__ = 'view_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='view_logs')
    post = db.relationship('Post', back_populates='view_logs')