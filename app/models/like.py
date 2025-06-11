from app import db
from datetime import datetime

class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id', ondelete='CASCADE'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    __table_args__ = (
        db.CheckConstraint(
            '(post_id IS NOT NULL AND comment_id IS NULL) OR (post_id IS NULL AND comment_id IS NOT NULL)',
            name='only_one_target_check'
        ),
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),
        db.UniqueConstraint('user_id', 'comment_id', name='unique_user_comment_like'),
    )

    user = db.relationship('User', backref='likes')
    post = db.relationship('Post', backref='likes', lazy='joined')
    comment = db.relationship('Comment', backref='likes', lazy='joined')