from flask import Blueprint, jsonify, request
from ..utils.db import load_db, save_db
from datetime import datetime, timedelta, timezone

showtimes_bp = Blueprint('showtimes', __name__)

@showtimes_bp.route('/showtimes', methods=['GET'])
def get_all_showtimes():
    db = load_db()
    seeded_showtimes = []
    
    for showtime in db['showtimes']:
        # Find the corresponding movie and theater
        movie = next((m for m in db['movies'] if m['id'] == showtime['movieId']), None)
        theater = next((t for t in db['theaters'] if t['id'] == showtime['theaterId']), None)
        
        # Create seeded showtime object
        seeded = {
            'id': showtime['id'],
            'time': showtime['time'],
            'price': showtime['price'],
            'movieTitle': movie['title'] if movie else None,
            'movieDuration': movie['duration'] if movie else None,
            'movieCast': movie['cast'] if movie else None,
            'movieGenre': movie['genre'] if movie else None,
            'theaterName': theater['name'] if theater else None,
            'theaterLocation': theater['location'] if theater else None,
            'availableSeats': theater['seatingCapacity'] - len(showtime.get('reservedSeats', {})) if theater else None
        }
        seeded_showtimes.append(seeded)
    
    return jsonify(seeded_showtimes), 200

@showtimes_bp.route('/showtimes/<int:showtime_id>', methods=['GET'])
def get_showtime(showtime_id):
    db = load_db()
    showtime = next((s for s in db['showtimes'] if s['id'] == showtime_id), None)
    
    if showtime is None:
        return jsonify({'error': 'Showtime not found'}), 404
    
    # seed showtime with movie and theater details
    movie = next((m for m in db['movies'] if m['id'] == showtime['movieId']), None)
    theater = next((t for t in db['theaters'] if t['id'] == showtime['theaterId']), None)
    
    response = {
        **showtime,
        'movie': movie,
        'theater': theater
    }
    
    return jsonify(response), 200

@showtimes_bp.route('/showtimes/<int:showtime_id>/reserve', methods=['POST'])
def reserve_seat(showtime_id):
    db = load_db()
    showtime = next((s for s in db['showtimes'] if s['id'] == showtime_id), None)
    
    if showtime is None:
        return jsonify({'error': 'Showtime not found'}), 404
    
    seat_id = request.args.get('seatId')
    
    if 'reservedSeats' not in showtime:
        showtime['reservedSeats'] = {}
    
    if seat_id in showtime['reservedSeats']:
        return jsonify({'error': 'Seat already reserved'}), 400
    
    ttl = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
    showtime['reservedSeats'][seat_id] = {
        'paid': False,
        'ttl': ttl
    }

    save_db(db)
    
    return jsonify({'message': 'Seat reserved successfully'}), 200
