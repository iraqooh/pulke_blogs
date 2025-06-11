from flask import Blueprint, request, jsonify
from app import db, jwt, logging
from app.models.user import User
from app.schemas.user_schema import RegisterSchema, LoginSchema, UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

logging.info('Creating Register, Login & User schemas')
register_schema = RegisterSchema()
login_schema = LoginSchema()
user_schema = UserSchema()

@auth_bp.route('/register', methods=['POST'])
def register():
    logging.info('Starting registration')
    data = register_schema.load(request.json)
    if User.query.filter((User.email == data['email']) | (User.username == data['username'])).first():
        logging.error('Email or username already exists')
        return jsonify({'error': 'Email or username already exists.'})
    
    user = User(email=data['email'], username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    logging.info(f'New user "{user.username}" created and saved to the database')
    return user_schema.jsonify(user), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    logging.info('Starting login')
    data = login_schema.load(request.json)
    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        logging.error('Invalid credentials')
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user': user_schema.dump(user)
    })

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    logging.info('Starting user profile access')
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user)

"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.post import Post

bp = Blueprint('users', __name__, url_prefix='/api/v1/users')

@bp.route('/<int:id>', methods=['GET'])
def get_user_profile(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'avatar_url': user.avatar_url,
        'bio': user.bio,
        'social_links': user.social_links
    }), 200


@bp.route('/<int:id>/posts', methods=['GET'])
def get_author_feed(id):
    posts = Post.query.filter_by(author_id=id, is_published=True).order_by(Post.created_at.desc()).all()
    return jsonify([p.to_dict() for p in posts]), 200


@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_profile(id):
    current_user_id = get_jwt_identity()['id']
    if current_user_id != id:
        return jsonify({'error': 'Unauthorized'}), 403

    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    user.avatar_url = data.get('avatar_url', user.avatar_url)
    user.bio = data.get('bio', user.bio)
    user.social_links = data.get('social_links', user.social_links)

    db.session.commit()
    return jsonify({'message': 'Profile updated'}), 200

"""