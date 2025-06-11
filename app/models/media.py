from app import db
from datetime import datetime

class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    file_url = db.Column(db.String(255), nullable=False)  # Local path or cloud URL
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.now)

    post = db.relationship('Post', back_populates='media')
