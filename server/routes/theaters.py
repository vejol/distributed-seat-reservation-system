from flask import Blueprint, jsonify
from ..utils.db import load_db

theaters_bp = Blueprint('theaters', __name__)

@theaters_bp.route('/theaters', methods=['GET'])
def get_all_theaters():
    db = load_db()
    return jsonify(db['theaters']), 200
