from pysyncobj import SyncObj, replicated
from typing import TypedDict

ActiveShowtimes = dict[int, dict[str, int]] # { showtimeID: { seatID: userID, seatID: userID ... } } 
# available seats have userID = None
TheaterRows = TypedDict('TheaterRows', {'row': str, 'seats': int})
# used in addShowTime, something for Application Servers to mind

class ReservationManager(SyncObj):
    def __init__(self, selfNodeAddr, otherNodeAddrs):
        super(ReservationManager, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.__activeShowtimes: ActiveShowtimes = {}

    def getFullState(self):
        return self.__activeShowtimes

    @replicated
    def addShowtime(self, showtimeID: int, rows: list[TheaterRows]):
        if showtimeID in self.__activeShowtimes:
            return {
                'success': False,
                'message': f'ERROR: Showtime with id {showtimeID} already exists.'
            }
    
        self.__activeShowtimes[showtimeID] = {}

        try:
            for row in rows:
                for n in range(row['seats']):
                    self.__activeShowtimes[showtimeID][f'{row["row"]}{n+1}'] = None
        except Exception as e:
            del self.__activeShowtimes[showtimeID]
            return {
                'success': False,
                'message': f'ERROR: {e}'
            }
        
        return {
            'success': True,
            'message': f'Showtime {showtimeID} successfully added!'
        }

    @replicated
    def removeShowtime(self, showtimeID: int):
        #TODO
        self.__activeShowtimes.pop(showtimeID)
        return self.__activeShowtimes

    def getShowtimes(self):
        return list(self.__activeShowtimes.keys())

    @replicated
    def reserveSeat(self, showtimeID: int, seatID: str, userID: int):
        if showtimeID not in self.__activeShowtimes:
            return {
                'success': False,
                'message': f'ERROR: Showtime with ID {showtimeID} does not exist.',
            }
        
        if seatID not in self.__activeShowtimes[showtimeID]:
            return {
                'success': False,
                'message': f'ERROR: Seat with ID {seatID} does not exist in showtime {showtimeID}.',
            }

        if self.__activeShowtimes[showtimeID][seatID] is not None:
            reserved_by = self.__activeShowtimes[showtimeID][seatID]
            return {
                'success': False,
                'message': f'ERROR reserving for user {userID}: Seat {seatID} for show {showtimeID} is already booked for user {reserved_by}.',
            }

        self.__activeShowtimes[showtimeID][seatID] = userID

        return {
            'success': True,
            'message': f'Seat {seatID} for showtime {showtimeID} successfully reserved for user {userID}!',
        }

    def getAvailableSeats(self, showtimeID: int):
        if showtimeID not in self.__activeShowtimes:
            return {
                'success': False,
                'message': f'ERROR: Showtime with ID {showtimeID} does not exist.'
            }

        try:
            availableSeats = []
            for seatID, userID in self.__activeShowtimes[showtimeID].items():
                if userID == None:
                    availableSeats.append(seatID)
        except Exception as e:
            return {
                'success': False,
                'message': f'ERROR: {e}'
            }

        return availableSeats
    
    def getAvailableShowtimes(self):
        # TODO this should return showtimes that have at least one free seat
        return
    
    def cancelSeat(self):
        # TODO
        return

    def getSeats(self, showtimeID: int):
        # TODO
        return
    
# DEV NOTE: you can copy-paste the line below (taken from db.json) when using addShowtime
# [{"row": "A","seats": 2},{"row": "B","seats": 2}]