from flask import Blueprint, request, jsonify
from app import db
from app.models.view import ViewLog
from app.models.post import Post
from app.models.user import User

views_bp = Blueprint('views', __name__, url_prefix='/api/v1/views')

@views_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    user_id = request.args.get('user_id')  

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    if user_id:
        view_log = ViewLog(user_id=user_id, post_id=post_id)
        db.session.add(view_log)
        db.session.commit()

    return jsonify(post.to_dict()), 200


@views_bp.route('/stats', methods=['GET'])
def get_view_stats():
    view_count = db.session.query(ViewLog.post_id, db.func.count(ViewLog.id)).group_by(ViewLog.post_id).all()
    stats = {post_id: count for post_id, count in view_count}

    return jsonify({"view_stats": stats}), 200


@views_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_views(user_id):
    views = ViewLog.query.filter_by(user_id=user_id).all()
    viewed_posts = [view.post.to_dict() for view in views]

    return jsonify({"viewed_posts": viewed_posts}), 200
