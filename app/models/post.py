from datetime import datetime
from slugify import slugify
from app import db, logging
from .tag import post_tags

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, index=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    content = db.Column(db.Text, nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', back_populates='posts')

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.slug = slugify(title)
        self.author_id = author_id

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'title': self.title,
            'content': self.content,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author_id': self.author_id,
        }

    bookmarked_by = db.relationship('Bookmark', back_populates='post', lazy='dynamic')
    view_logs = db.relationship('ViewLog', back_populates='post', lazy='dynamic')
    category = db.relationship('Category', back_populates='posts')
    tags = db.relationship('Tag', secondary=post_tags, lazy='dynamic')
    media = db.relationship('Media', back_populates='post', lazy='dynamic')