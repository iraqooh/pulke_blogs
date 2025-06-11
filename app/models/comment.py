from datetime import datetime
from app import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)

    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='joined')
    author = db.relationship('User')

    def to_dict(self, include_replies=True):
        data = {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'author_id': self.author_id,
            'post_id': self.post_id,
            'parent_id': self.parent_id,
        }
        if include_replies:
            data['replies'] = [r.to_dict() for r in self.replies]
        return data