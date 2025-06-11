from flask import Blueprint, jsonify
from app import db
from app.models.post import Post
from app.models.comment import Comment
from app.models.view import ViewLog

stats_bp = Blueprint('stats', __name__, url_prefix='/api/v1/stats')

@stats_bp.route('/posts', methods=['GET'])
def get_post_stats():
    total_posts = Post.query.count()
    return jsonify({'total_posts': total_posts}), 200

@stats_bp.route('/comments', methods=['GET'])
def get_comment_stats():
    total_comments = Comment.query.count()
    return jsonify({'total_comments': total_comments}), 200

@stats_bp.route('/views', methods=['GET'])
def get_view_stats():
    total_views = db.session.query(db.func.count(ViewLog.id)).scalar()
    return jsonify({'total_views': total_views}), 200

@stats_bp.route('/popular', methods=['GET'])
def get_popular_posts():
    popular_posts = db.session.query(
        Post.id, db.func.count(ViewLog.id).label('view_count')
    ).join(ViewLog).group_by(Post.id).order_by(db.desc('view_count')).limit(5).all()

    return jsonify([
        {'post_id': post_id, 'view_count': count} for post_id, count in popular_posts
    ]), 200
