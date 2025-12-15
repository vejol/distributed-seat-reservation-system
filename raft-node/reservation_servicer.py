import grpc
from time import sleep

import sys
from pathlib import Path
# Add parent directory to path BEFORE importing from rpc
sys.path.insert(0, str(Path(__file__).parent.parent))

from rpc import reservation_pb2, reservation_pb2_grpc, showtimes_pb2, showtimes_pb2_grpc


class ReservationServicer(reservation_pb2_grpc.ReservationServicer):
    """Implementation of the ReservationService."""

    def __init__(self, reservation_manager, node_address_map):
        self.reservation_manager = reservation_manager
        self.node_address_map = node_address_map  # Map of raft_address -> grpc_address

    def ReserveSeat(self, request, context):
        """Reserves a seat for a showtime."""
        # Check if this node is the leader
        if not self.reservation_manager._isLeader():
            # Forward to leader
            leader = self.reservation_manager._getLeader()
            if leader is None:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details("No leader elected yet. Please retry.")
                return reservation_pb2.ReserveSeatResponse(
                    success=False,
                    message="No leader available"
                )

            # Get leader's gRPC address
            leader_addr = str(leader.address) if hasattr(leader, 'address') else str(leader)
            leader_grpc = self.node_address_map.get(leader_addr)

            if not leader_grpc:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Leader address mapping not found: {leader_addr}")
                return reservation_pb2.ReserveSeatResponse(
                    success=False,
                    message="Leader address unknown"
                )

            print(f"[FOLLOWER] Forwarding ReserveSeat request to leader at {leader_grpc}")

            # Forward request to leader
            try:
                with grpc.insecure_channel(leader_grpc) as channel:
                    stub = reservation_pb2_grpc.ReservationServiceStub(channel)
                    response = stub.ReserveSeat(request)
                    print(f"[FOLLOWER] Received response from leader: {response.message}")
                    return response
            except Exception as e:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details(f"Failed to forward to leader: {str(e)}")
                return reservation_pb2.ReserveSeatResponse(
                    success=False,
                    message=f"Forward failed: {str(e)}"
                )

        # This node is the leader - process the request
        print(f"[LEADER] ReserveSeat: showtime_id={request.showtime_id}, seat_id={request.seat_id}, user_id={request.user_id}")
        
        result = self.reservation_manager.reserveSeat(
            request.showtime_id,
            request.seat_id,
            request.user_id
        )
        
        sleep(0.01)  # Allow replication to complete
        
        print(f"[LEADER] ReserveSeat result: {result}")
        return reservation_pb2.ReserveSeatResponse(
            success=result['success'],
            message=result['message']
        )

    def CancelSeat(self, request, context):
        """Cancels a seat reservation for a showtime."""
        # Check if this node is the leader
        if not self.reservation_manager._isLeader():
            # Forward to leader
            leader = self.reservation_manager._getLeader()
            if leader is None:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details("No leader elected yet. Please retry.")
                return reservation_pb2.CancelSeatResponse(
                    success=False,
                    message="No leader available"
                )

            # Get leader's gRPC address
            leader_addr = str(leader.address) if hasattr(leader, 'address') else str(leader)
            leader_grpc = self.node_address_map.get(leader_addr)

            if not leader_grpc:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Leader address mapping not found: {leader_addr}")
                return reservation_pb2.CancelSeatResponse(
                    success=False,
                    message="Leader address unknown"
                )

            print(f"[FOLLOWER] Forwarding CancelSeat request to leader at {leader_grpc}")

            # Forward request to leader
            try:
                with grpc.insecure_channel(leader_grpc) as channel:
                    stub = reservation_pb2_grpc.ReservationServiceStub(channel)
                    response = stub.CancelSeat(request)
                    print(f"[FOLLOWER] Received response from leader: {response.message}")
                    return response
            except Exception as e:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details(f"Failed to forward to leader: {str(e)}")
                return reservation_pb2.CancelSeatResponse(
                    success=False,
                    message=f"Forward failed: {str(e)}"
                )

        # This node is the leader - process the request
        print(f"[LEADER] CancelSeat: showtime_id={request.showtime_id}, seat_id={request.seat_id}")
        
        result = self.reservation_manager.cancelSeat(
            request.showtime_id,
            request.seat_id
        )
        
        sleep(0.01)  # Allow replication to complete
        
        print(f"[LEADER] CancelSeat result: {result}")
        return reservation_pb2.CancelSeatResponse(
            success=result['success'],
            message=result['message']
        )

    def GetAvailableSeats(self, request, context):
        """Gets available seats for a showtime (read operation - no leader forwarding needed)."""
        print(f"[NODE] GetAvailableSeats: showtime_id={request.showtime_id}")
        
        result = self.reservation_manager.getAvailableSeats(request.showtime_id)
        
        # Check if result is an error dict or a list
        if isinstance(result, dict):
            return reservation_pb2.GetAvailableSeatsResponse(
                success=result['success'],
                message=result['message'],
                seat_ids=[]
            )
        
        # Result is a list of seat IDs
        return reservation_pb2.GetAvailableSeatsResponse(
            success=True,
            message="Successfully retrieved available seats",
            seat_ids=result
        )

    def GetReservedSeats(self, request, context):
        """Gets reserved seats for a showtime (read operation - no leader forwarding needed)."""
        print(f"[NODE] GetReservedSeats: showtime_id={request.showtime_id}")
        
        result = self.reservation_manager.getReservedSeats(request.showtime_id)
        
        # Check if result is an error dict or a list
        if isinstance(result, dict):
            return reservation_pb2.GetReservedSeatsResponse(
                success=result['success'],
                message=result['message'],
                seat_ids=[]
            )
        
        # Result is a list of seat IDs
        return reservation_pb2.GetReservedSeatsResponse(
            success=True,
            message="Successfully retrieved reserved seats",
            seat_ids=result
        )


class ShowtimeServicer(showtimes_pb2_grpc.ShowtimeServicer):
    """Implementation of the ShowtimeService."""

    def __init__(self, reservation_manager, node_address_map):
        self.reservation_manager = reservation_manager
        self.node_address_map = node_address_map  # Map of raft_address -> grpc_address

    def AddShowtime(self, request, context):
        """Adds a new showtime with seating."""
        # Check if this node is the leader
        if not self.reservation_manager._isLeader():
            # Forward to leader
            leader = self.reservation_manager._getLeader()
            if leader is None:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details("No leader elected yet. Please retry.")
                return showtimes_pb2.AddShowtimeResponse(
                    success=False,
                    message="No leader available"
                )

            # Get leader's gRPC address
            leader_addr = str(leader.address) if hasattr(leader, 'address') else str(leader)
            leader_grpc = self.node_address_map.get(leader_addr)

            if not leader_grpc:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Leader address mapping not found: {leader_addr}")
                return showtimes_pb2.AddShowtimeResponse(
                    success=False,
                    message="Leader address unknown"
                )

            print(f"[FOLLOWER] Forwarding AddShowtime request to leader at {leader_grpc}")

            # Forward request to leader
            try:
                with grpc.insecure_channel(leader_grpc) as channel:
                    stub = showtimes_pb2_grpc.ShowtimeServiceStub(channel)
                    response = stub.AddShowtime(request)
                    print(f"[FOLLOWER] Received response from leader: {response.message}")
                    return response
            except Exception as e:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details(f"Failed to forward to leader: {str(e)}")
                return showtimes_pb2.AddShowtimeResponse(
                    success=False,
                    message=f"Forward failed: {str(e)}"
                )

        # This node is the leader - process the request
        print(f"[LEADER] AddShowtime: showtime_id={request.showtime_id}, rows={len(request.rows)}")
        
        # Convert protobuf rows to dict format expected by reservation_manager
        rows = [{'row': r.row, 'seats': r.seats} for r in request.rows]
        
        result = self.reservation_manager.addShowtime(
            request.showtime_id,
            rows
        )
        
        sleep(0.01)  # Allow replication to complete
        
        print(f"[LEADER] AddShowtime result: {result}")
        return showtimes_pb2.AddShowtimeResponse(
            success=result['success'],
            message=result['message']
        )

    def RemoveShowtime(self, request, context):
        """Removes a showtime."""
        # Check if this node is the leader
        if not self.reservation_manager._isLeader():
            # Forward to leader
            leader = self.reservation_manager._getLeader()
            if leader is None:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details("No leader elected yet. Please retry.")
                return showtimes_pb2.RemoveShowtimeResponse(
                    success=False,
                    message="No leader available"
                )

            # Get leader's gRPC address
            leader_addr = str(leader.address) if hasattr(leader, 'address') else str(leader)
            leader_grpc = self.node_address_map.get(leader_addr)

            if not leader_grpc:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details(f"Leader address mapping not found: {leader_addr}")
                return showtimes_pb2.RemoveShowtimeResponse(
                    success=False,
                    message="Leader address unknown"
                )

            print(f"[FOLLOWER] Forwarding RemoveShowtime request to leader at {leader_grpc}")

            # Forward request to leader
            try:
                with grpc.insecure_channel(leader_grpc) as channel:
                    stub = showtimes_pb2_grpc.ShowtimeServiceStub(channel)
                    response = stub.RemoveShowtime(request)
                    print(f"[FOLLOWER] Received response from leader: {response.message}")
                    return response
            except Exception as e:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details(f"Failed to forward to leader: {str(e)}")
                return showtimes_pb2.RemoveShowtimeResponse(
                    success=False,
                    message=f"Forward failed: {str(e)}"
                )

        # This node is the leader - process the request
        print(f"[LEADER] RemoveShowtime: showtime_id={request.showtime_id}")
        
        result = self.reservation_manager.removeShowtime(request.showtime_id)
        
        sleep(0.01)  # Allow replication to complete
        
        print(f"[LEADER] RemoveShowtime result: {result}")
        return showtimes_pb2.RemoveShowtimeResponse(
            success=result['success'],
            message=result['message']
        )

    def GetShowtimes(self, request, context):
        """Gets all showtimes (read operation - no leader forwarding needed)."""
        print(f"[NODE] GetShowtimes: retrieving all showtimes")
        
        showtime_ids = self.reservation_manager.getShowtimes()
        
        print(f"[NODE] GetShowtimes result: {showtime_ids}")
        return showtimes_pb2.GetShowtimesResponse(
            showtime_ids=showtime_ids
        )
