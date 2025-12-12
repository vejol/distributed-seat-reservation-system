from flask import Blueprint, jsonify
import grpc

from rpc import pingpong_pb2
from rpc import pingpong_pb2_grpc

health_bp = Blueprint('health', __name__)

# gRPC client connection
channel = grpc.insecure_channel('localhost:50001')
ping_stub = pingpong_pb2_grpc.PingPongStub(channel)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'message': 'pong'}), 200


@health_bp.route('/ping', methods=['GET'])
def ping():
    """Ping endpoint for testing gRPC connection"""
    try:        
        # Call gRPC service
        grpc_request = pingpong_pb2.PingRequest(message='Ping!')
        grpc_response = ping_stub.Ping(grpc_request)

        return jsonify({
            'success': True,
            'response': grpc_response.message
        })
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
    