from .cluster_config import get_addresses, parse_args
from .reservation_manager import ReservationManager
from .ping_servicer import PingPongServicer

import grpc
from concurrent import futures
import time

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from rpc import pingpong_pb2_grpc


def main():
    args = parse_args()
    selfAddr, partners = get_addresses(args)
    grpc_port = int(50000 + args.id)
    node_map = {i: addr for i, addr in enumerate([selfAddr] + partners)}

    globalState = ReservationManager(selfAddr, partners)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pingpong_pb2_grpc.add_PingPongServicer_to_server(
        PingPongServicer(globalState, node_map or {}), 
        server
    )

    server.add_insecure_port(f"[::]:{grpc_port}")
    server.start()

    print(f"gRPC Server started on port {grpc_port}")
    print("Waiting for ping requests...")
    print(f"Current ping count: {globalState.get_count()}")
    print("-" * 50)

    try:
        while True:
            time.sleep(86400)  # Keep server running
    except KeyboardInterrupt:
        print(f"\nShutting down server... (Final count: {globalState.get_count()})")
        server.stop(0)

    

if __name__ == "__main__":
    main()