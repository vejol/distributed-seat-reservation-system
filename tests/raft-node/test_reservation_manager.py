"""
Test suite for Raft node ReservationManager
"""
import pytest
import sys
import time
from pathlib import Path

# Add raft-node directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'raft-node'))

from reservation_manager import ReservationManager


@pytest.fixture
def manager():
    """Create a single-node Raft manager for testing"""
    def on_seat_map_changed(manager):
        """Callback for seat map changes"""
        pass
    
    # Create a single-node cluster for testing
    mgr = ReservationManager(
        selfNodeAddr="localhost:7000",
        otherNodeAddrs=[],  # Single node
        on_seat_map_changed=on_seat_map_changed,
        initialShowTimes={},
        diskJournal=False  # Disable disk persistence for tests
    )
    
    # Wait for initialization
    time.sleep(0.5)
    
    yield mgr
    
    # Cleanup
    mgr._destroy()


class TestReservationManager:
    """Test suite for ReservationManager"""
    
    def test_add_showtime(self, manager):
        """Test adding a new showtime"""
        # Arrange
        showtime_id = 1
        rows = [
            {"row": "a", "seats": 3},
            {"row": "b", "seats": 2}
        ]
        
        # Act
        manager.addShowtime(showtime_id, rows)
        time.sleep(1.0)  # Wait for Raft replication
        
        # Assert - verify showtime exists by checking state
        showtimes = manager.getShowtimes()
        assert showtime_id in showtimes
        
        # Verify we can get the full state
        state = manager.getFullState()
        assert showtime_id in state
        assert "a1" in state[showtime_id]
        assert "b1" in state[showtime_id]
    
    def test_reserve_seat_success(self, manager):
        """Test successful seat reservation"""
        # Arrange
        showtime_id = 1
        rows = [{"row": "a", "seats": 3}]
        manager.addShowtime(showtime_id, rows)
        time.sleep(1.0)
        
        # Act
        manager.reserveSeat(
            showtimeID=showtime_id,
            seatID="a1",
            userID=100
        )
        time.sleep(1.0)
        
        # Assert - check the state directly
        state = manager.getFullState()
        assert state[showtime_id]["a1"] == 100
    
    def test_reserve_already_booked_seat(self, manager):
        """Test reserving an already booked seat"""
        # Arrange
        showtime_id = 1
        rows = [{"row": "a", "seats": 2}]
        manager.addShowtime(showtime_id, rows)
        time.sleep(1.0)
        
        # First reservation
        manager.reserveSeat(showtime_id, "a1", 100)
        time.sleep(1.0)
        
        # Verify first reservation worked
        state = manager.getFullState()
        assert state[showtime_id]["a1"] == 100
        
        # Act - try to book same seat
        manager.reserveSeat(showtime_id, "a1", 200)
        time.sleep(1.0)
        
        # Assert - seat should still belong to user 100
        state = manager.getFullState()
        assert state[showtime_id]["a1"] == 100  # Not changed
    
    def test_cancel_seat(self, manager):
        """Test canceling a seat reservation"""
        # Arrange
        showtime_id = 1
        rows = [{"row": "a", "seats": 2}]
        manager.addShowtime(showtime_id, rows)
        time.sleep(1.0)
        
        manager.reserveSeat(showtime_id, "a1", 100)
        time.sleep(1.0)
        
        # Act
        manager.cancelSeat(showtime_id, "a1")
        time.sleep(1.0)
        
        # Assert - seat should be available (None)
        state = manager.getFullState()
        assert state[showtime_id]["a1"] is None
    
    def test_get_showtimes(self, manager):
        """Test getting list of showtimes"""
        # Arrange
        manager.addShowtime(1, [{"row": "a", "seats": 2}])
        time.sleep(1.0)
        manager.addShowtime(2, [{"row": "b", "seats": 3}])
        time.sleep(1.0)
        
        # Act
        showtimes = manager.getShowtimes()
        
        # Assert
        assert 1 in showtimes
        assert 2 in showtimes
        assert len(showtimes) == 2
    
    def test_get_custom_status(self, manager):
        """Test getting Raft cluster status"""
        # Act
        status = manager.getCustomStatus()
        
        # Assert
        assert 'state' in status
        assert 'leader' in status
        assert 'has_quorum' in status
        assert 'raft_term' in status
        
        # Single node should have quorum
        assert status['has_quorum'] is True
