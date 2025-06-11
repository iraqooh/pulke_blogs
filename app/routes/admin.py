from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.post import Post

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()['id']
        user = User.query.get(user_id)
        if not user or not user.is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/posts', methods=['GET'])
@admin_required
def get_all_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email, 'role': u.role.value} for u in users]), 200

@admin_bp.route('/reports', methods=['GET'])
@admin_required
def get_reports():
    from app.models.view import ViewLog
    popular_posts = db.session.query(Post.id, db.func.count(ViewLog.id).label('views')).join(ViewLog).group_by(Post.id).order_by(db.desc('views')).limit(5).all()
    return jsonify({'popular_posts': [{'id': p_id, 'views': v} for p_id, v in popular_posts]}), 200

import csv
from flask import Response

@admin_bp.route('/export/posts', methods=['GET'])
@admin_required
def export_posts():
    posts = Post.query.all()
    csv_data = [['ID', 'Title', 'Author', 'Published']]
    
    for post in posts:
        csv_data.append([post.id, post.title, post.author.username, post.is_published])
    
    def generate():
        for row in csv_data:
            yield ','.join(map(str, row)) + '\n'

    return Response(generate(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=posts.csv'})

