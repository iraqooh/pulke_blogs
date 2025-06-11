from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.comment import Comment
from models.post import Post
from app import db

bp = Blueprint('comments', __name__, url_prefix='/api/v1')

@bp.route('/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    data = request.get_json()
    content = data.get('content')
    parent_id = data.get('parent_id')
    user_id = get_jwt_identity()['id']

    if not content:
        return jsonify({'error': 'Comment content is required'}), 400

    if not Post.query.get(post_id):
        return jsonify({'error': 'Post not found'}), 404

    comment = Comment(content=content, post_id=post_id, author_id=user_id, parent_id=parent_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@bp.route('/posts/<int:post_id>/comments', methods=['GET'])
def list_comments(post_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Comment.query.filter_by(post_id=post_id, parent_id=None).order_by(Comment.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    top_comments = pagination.items

    return jsonify({
        'comments': [c.to_dict() for c in top_comments],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200

@bp.route('/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def edit_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    user_id = get_jwt_identity()['id']
    if user_id != comment.author_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    comment.content = data.get('content', comment.content)
    db.session.commit()
    return jsonify(comment.to_dict()), 200

@bp.route('/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404

    user_id = get_jwt_identity()['id']
    if user_id != comment.author_id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': 'Comment deleted'}), 200