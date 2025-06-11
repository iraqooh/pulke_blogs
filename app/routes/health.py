from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__, url_prefix='/api/v1')

@health_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'Pulke Blogs API is up and running'}), 200