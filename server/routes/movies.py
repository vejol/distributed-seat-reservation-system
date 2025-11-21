from flask import Blueprint, jsonify
from utils.db import load_db

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/movies', methods=['GET'])
def get_all_movies():
    db = load_db()
    return jsonify(db['movies']), 200
