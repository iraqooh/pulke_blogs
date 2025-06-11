from flask import Blueprint, request, jsonify
from app import db
from app.models.bookmark import Bookmark
from app.models.post import Post
from app.models.user import User

bookmarks_bp = Blueprint('bookmarks', __name__, url_prefix='/api/v1/bookmarks')

@bookmarks_bp.route('/<int:post_id>', methods=['POST'])
def add_bookmark(post_id):
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    if not user or not post:
        return jsonify({"error": "Invalid user or post"}), 404

    if Bookmark.query.filter_by(user_id=user_id, post_id=post_id).first():
        return jsonify({"message": "Already bookmarked"}), 409

    bookmark = Bookmark(user_id=user_id, post_id=post_id)
    db.session.add(bookmark)
    db.session.commit()

    return jsonify({"message": "Post bookmarked successfully"}), 201


@bookmarks_bp.route('/<int:post_id>', methods=['DELETE'])
def remove_bookmark(post_id):
    user_id = request.json.get('user_id')
    bookmark = Bookmark.query.filter_by(user_id=user_id, post_id=post_id).first()

    if not bookmark:
        return jsonify({"error": "Bookmark not found"}), 404

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({"message": "Bookmark removed"}), 200


@bookmarks_bp.route('/user/<int:user_id>', methods=['GET'])
def get_bookmarks(user_id):
    bookmarks = Bookmark.query.filter_by(user_id=user_id).all()
    bookmarked_posts = [bookmark.post.to_dict() for bookmark in bookmarks]

    return jsonify({"bookmarks": bookmarked_posts}), 200
