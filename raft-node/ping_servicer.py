import grpc
from time import sleep

import sys
from pathlib import Path
# Add parent directory to path BEFORE importing from rpc
sys.path.insert(0, str(Path(__file__).parent.parent))

from rpc import pingpong_pb2, pingpong_pb2_grpc

class PingPongServicer(pingpong_pb2_grpc.PingPongServicer):
    """Implementation of the PingPong service."""

    def __init__(self, counter, node_address_map):
        self.counter = counter
        self.node_address_map = node_address_map  # Map of raft_address -> grpc_address

    def Ping(self, request, context):
        """Responds to a ping request with a pong."""
        # Check if this node is the leader
        if not self.counter._isLeader():
            # Forward to leader
            leader = self.counter._getLeader()
            if leader is None:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details("No leader elected yet. Please retry.")
                return pingpong_pb2.PongResponse(message="No leader available")

            # Get leader's gRPC address
            leader_addr = str(leader.address) if hasattr(leader, 'address') else str(leader)
            leader_grpc = self.node_address_map.get(leader_addr)

            if not leader_grpc:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Leader address mapping not found: {leader_addr}")
                return pingpong_pb2.PongResponse(message="Leader address unknown")

            print(f"[FOLLOWER] Forwarding request to leader at {leader_grpc}")

            # Forward request to leader
            try:
                with grpc.insecure_channel(leader_grpc) as channel:
                    stub = pingpong_pb2_grpc.PingPongStub(channel)
                    response = stub.Ping(request)
                    print(f"[FOLLOWER] Received response from leader: {response.message}")
                    return response
            except Exception as e:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details(f"Failed to forward to leader: {str(e)}")
                return pingpong_pb2.PongResponse(message=f"Forward failed: {str(e)}")

        # This node is the leader - process the request
        self.counter._increment()
        sleep(0.01)  # Allow replication to complete
        count = self.counter.get_count()

        print(f"[LEADER] Received: {request.message} (Count: {count})")
        response_message = f"Pong! (received: '{request.message}', count: {count})"
        print(f"[LEADER] Sending: {response_message}")
        return pingpong_pb2.PongResponse(message=response_message)