from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')

@categories_bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories]), 200

@categories_bp.route('', methods=['POST'])
def add_category():
    data = request.json
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category added'}), 201

@categories_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    category.name = request.json['name']
    db.session.commit()
    return jsonify({'message': 'Category updated'}), 200

@categories_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted'}), 200
