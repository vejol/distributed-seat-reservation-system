from flask import Blueprint, jsonify
from utils.db import load_db

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/movies', methods=['GET'])
def get_all_movies():
    db = load_db()
    return jsonify(db['movies']), 200

@movies_bp.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    db = load_db()
    movie = next((m for m in db['movies'] if m['id'] == movie_id), None)
    
    if movie is None:
        return jsonify({'error': 'Movie not found'}), 404
    
    return jsonify(movie), 200
