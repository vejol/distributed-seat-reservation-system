"""
Test suite for Raft node ReservationManager
"""
import pytest
import time

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
        otherNodeAddrs=[],
        on_seat_map_changed=on_seat_map_changed,
        initialShowTimes={},
        diskLogsAndSnapshots=False
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
        
        # Assert: verify showtime exists by checking state
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
        
        # Assert: check the state directly
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
        
        # Act: try to book same seat
        manager.reserveSeat(showtime_id, "a1", 200)
        time.sleep(1.0)
        
        # Assert: seat should still belong to user 100
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
        
        # Assert: seat should be available (None)
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
    
    def test_remove_showtime(self, manager):
        """Test removing a showtime"""
        # Arrange
        manager.addShowtime(1, [{"row": "a", "seats": 2}])
        time.sleep(1.0)
        
        # Act
        manager.removeShowtime(1)
        time.sleep(1.0)
        
        # Assert
        showtimes = manager.getShowtimes()
        assert 1 not in showtimes
    
    def test_remove_nonexistent_showtime(self, manager):
        """Test removing a showtime that doesn't exist"""
        # Act
        manager.removeShowtime(999)
        time.sleep(1.0)
        
        # Assert: verify nothing changed
        showtimes = manager.getShowtimes()
        assert len(showtimes) == 0
    
    def test_get_available_seats(self, manager):
        """Test getting available seats"""
        # Arrange
        manager.addShowtime(1, [{"row": "a", "seats": 3}])
        time.sleep(1.0)
        manager.reserveSeat(1, "a1", 100)
        time.sleep(1.0)
        
        # Act
        available = manager.getAvailableSeats(1)
        
        # Assert
        assert "a2" in available
        assert "a3" in available
        assert "a1" not in available
        assert len(available) == 2
    
    def test_get_available_seats_nonexistent_showtime(self, manager):
        """Test getting available seats for non-existent showtime"""
        # Act
        result = manager.getAvailableSeats(999)
        
        # Assert
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'does not exist' in result['message']
    
    def test_get_reserved_seats(self, manager):
        """Test getting reserved seats"""
        # Arrange
        manager.addShowtime(1, [{"row": "a", "seats": 3}])
        time.sleep(1.0)
        manager.reserveSeat(1, "a1", 100)
        manager.reserveSeat(1, "a2", 200)
        time.sleep(1.0)
        
        # Act
        reserved = manager.getReservedSeats(1)
        
        # Assert
        assert "a1" in reserved
        assert "a2" in reserved
        assert "a3" not in reserved
        assert len(reserved) == 2
    
    def test_get_reserved_seats_nonexistent_showtime(self, manager):
        """Test getting reserved seats for non-existent showtime"""
        # Act
        result = manager.getReservedSeats(999)
        
        # Assert
        assert isinstance(result, dict)
        assert result['success'] is False
        assert 'does not exist' in result['message']
    
    def test_add_duplicate_showtime(self, manager):
        """Test adding a showtime with duplicate ID"""
        # Arrange
        manager.addShowtime(1, [{"row": "a", "seats": 2}])
        time.sleep(1.0)
        
        # Act
        manager.addShowtime(1, [{"row": "b", "seats": 3}])
        time.sleep(1.0)
        
        # Assert: verify original showtime wasn't replaced
        state = manager.getFullState()
        assert 1 in state
        assert "a1" in state[1]  # Original seats
        assert "b1" not in state[1]  # New seats shouldn't exist
    
    def test_reserve_seat_invalid_showtime(self, manager):
        """Test reserving seat for non-existent showtime"""
        # Act
        manager.reserveSeat(999, "a1", 100)
        time.sleep(1.0)
        
        # Assert: verify state unchanged
        state = manager.getFullState()
        assert 999 not in state
    
    def test_reserve_seat_invalid_seat(self, manager):
        """Test reserving non-existent seat"""
        # Arrange
        manager.addShowtime(1, [{"row": "a", "seats": 2}])
        time.sleep(1.0)
        
        # Act
        manager.reserveSeat(1, "z99", 100)
        time.sleep(1.0)
        
        # Assert: verify invalid seat not added
        state = manager.getFullState()
        assert "z99" not in state[1]
    
    def test_cancel_seat_invalid_showtime(self, manager):
        """Test canceling seat for non-existent showtime"""
        # Act
        manager.cancelSeat(999, "a1")
        time.sleep(1.0)
        
        # Assert: verify nothing changed
        state = manager.getFullState()
        assert 999 not in state
    
    def test_cancel_seat_invalid_seat(self, manager):
        """Test canceling non-existent seat"""
        # Arrange
        manager.addShowtime(1, [{"row": "a", "seats": 2}])
        time.sleep(1.0)
        
        # Act
        manager.cancelSeat(1, "z99")
        time.sleep(1.0)
        
        # Assert: verify state unchanged (seats still None)
        state = manager.getFullState()
        assert state[1]["a1"] is None
        assert state[1]["a2"] is None
    
    def test_cancel_unreserved_seat(self, manager):
        """Test canceling a seat that isn't reserved"""
        # Arrange
        manager.addShowtime(1, [{"row": "a", "seats": 2}])
        time.sleep(1.0)
        
        # Act
        manager.cancelSeat(1, "a1")
        time.sleep(1.0)
        
        # Assert: seat should still be None (not reserved)
        state = manager.getFullState()
        assert state[1]["a1"] is None
    
    def test_add_showtime_empty_rows(self, manager):
        """Test adding a showtime with empty rows array"""
        # Act
        manager.addShowtime(1, [])
        time.sleep(1.0)
        
        # Assert
        showtimes = manager.getShowtimes()
        assert 1 in showtimes
        state = manager.getFullState()
        assert len(state[1]) == 0
    
    def test_add_showtime_invalid_row_structure(self, manager):
        """Test adding a showtime with invalid row structure"""
        # Act: missing 'seats' key
        manager.addShowtime(1, [{"row": "a"}])
        time.sleep(1.0)
        
        # Assert: showtime should not be created due to error
        showtimes = manager.getShowtimes()
        assert 1 not in showtimes
    
    def test_multiple_users_different_seats(self, manager):
        """Test multiple users reserving different seats"""
        # Arrange
        manager.addShowtime(1, [{"row": "a", "seats": 3}])
        time.sleep(1.0)
        
        # Act
        manager.reserveSeat(1, "a1", 100)
        manager.reserveSeat(1, "a2", 200)
        manager.reserveSeat(1, "a3", 300)
        time.sleep(1.0)
        
        # Assert
        state = manager.getFullState()
        assert state[1]["a1"] == 100
        assert state[1]["a2"] == 200
        assert state[1]["a3"] == 300
