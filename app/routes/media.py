import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app import db, app
from app.models.media import Media
from app.models.post import Post

media_bp = Blueprint('media', __name__, url_prefix='/api/v1/media')

UPLOAD_FOLDER = 'uploads/'  # Local storage folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@media_bp.route('/upload', methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    post_id = request.form.get('post_id')

    if not post_id or not Post.query.get(post_id):
        return jsonify({'error': 'Invalid post ID'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    media = Media(file_url=file_path, post_id=post_id)
    db.session.add(media)
    db.session.commit()

    return jsonify({'message': 'File uploaded', 'file_url': file_path}), 201

@media_bp.route('/<int:media_id>', methods=['GET'])
def get_media(media_id):
    media = Media.query.get(media_id)
    if not media:
        return jsonify({'error': 'Media not found'}), 404

    return jsonify({'file_url': media.file_url}), 200
