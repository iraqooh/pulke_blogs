from flask import Blueprint, request, jsonify
from app import db
from app.models.tag import Tag

tags_bp = Blueprint('tags', __name__, url_prefix='/api/v1/tags')

@tags_bp.route('', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([{'id': t.id, 'name': t.name} for t in tags]), 200

@tags_bp.route('', methods=['POST'])
def add_tag():
    data = request.json
    tag = Tag(name=data['name'])
    db.session.add(tag)
    db.session.commit()
    return jsonify({'message': 'Tag added'}), 201

@tags_bp.route('/<int:id>', methods=['DELETE'])
def delete_tag(id):
    tag = Tag.query.get(id)
    if not tag:
        return jsonify({'error': 'Tag not found'}), 404
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Tag deleted'}), 200
