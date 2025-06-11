from flask import Blueprint, jsonify, request
from app import db
from app.models import Post, Comment, Like
from flask_jwt_extended import jwt_required, get_jwt_identity

likes_bp = Blueprint('likes', __name__)

@likes_bp.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()
    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if like:
        return jsonify({'message': 'Already liked'}), 400
    new_like = Like(user_id=user_id, post_id=post_id)
    db.session.add(new_like)
    db.session.commit()
    return jsonify({'message': 'Post liked'}), 201

@likes_bp.route('/posts/<int:post_id>/like', methods=['DELETE'])
@jwt_required()
def unlike_post(post_id):
    user_id = get_jwt_identity()
    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if not like:
        return jsonify({'message': 'Not liked yet'}), 404
    db.session.delete(like)
    db.session.commit()
    return jsonify({'message': 'Post unliked'})

@likes_bp.route('/posts/<int:post_id>/likes', methods=['GET'])
def get_post_likes(post_id):
    count = Like.query.filter_by(post_id=post_id).count()
    return jsonify({'likes': count})