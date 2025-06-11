# app/models/bookmark.py
from app import db
from datetime import datetime

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    user = db.relationship('User', back_populates='bookmarks')
    post = db.relationship('Post', back_populates='bookmarked_by')

