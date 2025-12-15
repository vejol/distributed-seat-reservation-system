from flask import Blueprint, jsonify, request
from ..utils.db import load_db, save_db
from datetime import datetime, timedelta, timezone
import grpc

from rpc import showtimes_pb2
from rpc import showtimes_pb2_grpc
from rpc import reservation_pb2
from rpc import reservation_pb2_grpc

showtimes_bp = Blueprint('showtimes', __name__)

# gRPC client connections
channel = grpc.insecure_channel('localhost:50001')
showtime_stub = showtimes_pb2_grpc.ShowtimeStub(channel)
reservation_stub = reservation_pb2_grpc.ReservationStub(channel)

@showtimes_bp.route('/showtimes', methods=['GET'])
def get_all_showtimes():
    """Get all showtimes with gRPC integration"""
    try:
        # Call gRPC service to get active showtimes
        grpc_request = showtimes_pb2.GetShowtimesRequest()
        grpc_response = showtime_stub.GetShowtimes(grpc_request)
        
        db = load_db()
        seeded_showtimes = []
        
        # Filter showtimes by those active in gRPC
        active_showtime_ids = set(grpc_response.showtime_ids)
        
        for showtime in db['showtimes']:
            if showtime['id'] not in active_showtime_ids:
                continue
                
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
    except grpc.RpcError as e:
        return jsonify({
            'success': False,
            'error': f'{e.code()}: {e.details()}'
        }), 503
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@showtimes_bp.route('/showtimes/<int:showtime_id>', methods=['GET'])
def get_showtime(showtime_id):
    """Get specific showtime with gRPC integration"""
    try:
        # Call gRPC service to verify showtime exists
        grpc_request = showtimes_pb2.GetShowtimesRequest()
        grpc_response = showtime_stub.GetShowtimes(grpc_request)
        
        if showtime_id not in grpc_response.showtime_ids:
            return jsonify({'error': 'Showtime not found or not active'}), 404
        
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
    except grpc.RpcError as e:
        return jsonify({
            'success': False,
            'error': f'{e.code()}: {e.details()}'
        }), 503
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@showtimes_bp.route('/showtimes/<int:showtime_id>/reserve', methods=['POST'])
def reserve_seat(showtime_id):
    """Reserve a seat with gRPC integration"""
    try:
        seat_id = request.args.get('seatId')
        user_id = request.args.get('userId', type=int, default=1)  # Default user_id if not provided
        
        if not seat_id:
            return jsonify({'error': 'seatId is required'}), 400
        
        # Call gRPC service to reserve the seat
        grpc_request = reservation_pb2.ReserveSeatRequest(
            showtime_id=showtime_id,
            seat_id=seat_id,
            user_id=user_id
        )
        grpc_response = reservation_stub.ReserveSeat(grpc_request)
        
        if not grpc_response.success:
            return jsonify({'error': grpc_response.message}), 400
        
        # Update local database for TTL tracking
        db = load_db()
        showtime = next((s for s in db['showtimes'] if s['id'] == showtime_id), None)
        
        if showtime is None:
            return jsonify({'error': 'Showtime not found'}), 404
        
        if 'reservedSeats' not in showtime:
            showtime['reservedSeats'] = {}
        
        ttl = (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat()
        showtime['reservedSeats'][seat_id] = {
            'paid': False,
            'ttl': ttl,
            'userId': user_id
        }

        save_db(db)
        
        return jsonify({
            'success': True,
            'message': grpc_response.message
        }), 200
    except grpc.RpcError as e:
        return jsonify({
            'success': False,
            'error': f'{e.code()}: {e.details()}'
        }), 503
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@showtimes_bp.route('/showtimes/<int:showtime_id>/cancel', methods=['POST'])
def cancel_seat(showtime_id):
    """Cancel a seat reservation with gRPC integration"""
    try:
        seat_id = request.args.get('seatId')
        
        if not seat_id:
            return jsonify({'error': 'seatId is required'}), 400
        
        # Call gRPC service to cancel the seat
        grpc_request = reservation_pb2.CancelSeatRequest(
            showtime_id=showtime_id,
            seat_id=seat_id
        )
        grpc_response = reservation_stub.CancelSeat(grpc_request)
        
        if not grpc_response.success:
            return jsonify({'error': grpc_response.message}), 400
        
        # Update local database
        db = load_db()
        showtime = next((s for s in db['showtimes'] if s['id'] == showtime_id), None)
        
        if showtime and 'reservedSeats' in showtime and seat_id in showtime['reservedSeats']:
            del showtime['reservedSeats'][seat_id]
            save_db(db)
        
        return jsonify({
            'success': True,
            'message': grpc_response.message
        }), 200
    except grpc.RpcError as e:
        return jsonify({
            'success': False,
            'error': f'{e.code()}: {e.details()}'
        }), 503
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
