from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200
