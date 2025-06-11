from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.notification import Notification
from app.models.user import User

bp = Blueprint('notifications', __name__, url_prefix='/api/v1/notifications')

@bp.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe():
    user_id = get_jwt_identity()['id']
    return jsonify({'message': f'User {user_id} subscribed successfully'}), 200


@bp.route('', methods=['GET'])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()['id']
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
    return jsonify([{'id': n.id, 'message': n.message, 'created_at': n.created_at} for n in notifications]), 200


@bp.route('/<int:id>/read', methods=['PATCH'])
@jwt_required()
def mark_as_read(id):
    user_id = get_jwt_identity()['id']
    notification = Notification.query.filter_by(id=id, user_id=user_id).first()

    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    notification.is_read = True
    db.session.commit()

    return jsonify({'message': 'Notification marked as read'}), 200


@bp.route('/posts/<int:post_id>/notify', methods=['POST'])
def send_post_notification(post_id):
    message = f"New post published: {post_id}"
    subscribers = User.query.all()

    for user in subscribers:
        notification = Notification(user_id=user.id, message=message)
        db.session.add(notification)

    db.session.commit()
    return jsonify({'message': 'Notifications sent'}), 201
