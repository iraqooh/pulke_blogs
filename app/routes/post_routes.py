from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models.post import Post
from models.user import User
from models.category import Category
from models.tag import Tag
from flask_limiter import Limiter

bp = Blueprint('posts', __name__, url_prefix='/api/v1/posts')

@bp.route('', methods=['GET'])
@Limiter.limit("10 per minute")
def get_posts():
    category_id = request.args.get('category_id')
    tag_id = request.args.get('tag_id')

    query = Post.query.filter_by(is_published=True)

    if category_id:
        query = query.filter_by(category_id=category_id)

    if tag_id:
        query = query.filter(Post.tags.any(id=tag_id))

    posts = query.order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200


@bp.route('/<slug>', methods=['GET'])
def get_post(slug):
    post = Post.query.filter_by(slug=slug, is_published=True).first()
    if not post:
        return jsonify({'error': 'Post not found or unpublished'}), 404

    # Auto-log view
    user_id = request.args.get('user_id')
    if user_id:
        from models.view import ViewLog
        view_log = ViewLog(user_id=user_id, post_id=post.id)
        db.session.add(view_log)
        db.session.commit()

    return jsonify(post.to_dict()), 200


@bp.route('', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    current_user_id = get_jwt_identity()['id']

    title = data.get('title')
    content = data.get('content')
    category_id = data.get('category_id')
    tag_ids = data.get('tag_ids', [])

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    post = Post(title=title, content=content, author_id=current_user_id)

    # Assign category
    if category_id:
        category = Category.query.get(category_id)
        if category:
            post.category = category

    # Assign tags
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        post.tags.extend(tags)

    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict()), 201


@bp.route('/<slug>', methods=['PUT'])
@jwt_required()
def update_post(slug):
    current_user_id = get_jwt_identity()['id']
    post = Post.query.filter_by(slug=slug).first()

    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post.author_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    category_id = data.get('category_id')
    tag_ids = data.get('tag_ids', [])

    # Update category
    if category_id:
        category = Category.query.get(category_id)
        if category:
            post.category = category

    # Update tags
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.commit()
    return jsonify(post.to_dict()), 200


@bp.route('/<slug>', methods=['DELETE'])
@jwt_required()
def delete_post(slug):
    current_user_id = get_jwt_identity()['id']
    post = Post.query.filter_by(slug=slug).first()

    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post.author_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted'}), 200


@bp.route('/drafts', methods=['GET'])
@jwt_required()
def get_user_drafts():
    current_user_id = get_jwt_identity()['id']
    drafts = Post.query.filter_by(author_id=current_user_id, is_published=False).all()
    return jsonify([p.to_dict() for p in drafts]), 200


@bp.route('/<slug>/publish', methods=['PATCH'])
@jwt_required()
def toggle_publish(slug):
    current_user_id = get_jwt_identity()['id']
    post = Post.query.filter_by(slug=slug).first()

    if not post:
        return jsonify({'error': 'Post not found'}), 404
    if post.author_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    post.is_published = not post.is_published
    db.session.commit()
    return jsonify({
        'message': 'Post published' if post.is_published else 'Post unpublished',
        'is_published': post.is_published
    }), 200
