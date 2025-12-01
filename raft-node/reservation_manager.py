from pysyncobj import SyncObj, replicated
from typing import TypedDict
ActiveShowtimes = dict[int, dict[str, int]]
# { showtimeID: { seatID: userID } }
TheaterRows = TypedDict('TheaterRows', {'row': str, 'seats': int})

class ReservationManager(SyncObj):
    def __init__(self, selfNodeAddr, otherNodeAddrs):
        super(ReservationManager, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.__activeShowtimes: ActiveShowtimes = {}

    @replicated
    def addShowtime(self, showtimeID: int, rows: list[TheaterRows]):
        if showtimeID not in self.__activeShowtimes:
            self.__activeShowtimes[showtimeID] = {}

        for row in rows:
            for n in range(row['seats']):
                self.__activeShowtimes[showtimeID][f'{row["row"]}{n+1}'] = None
                
        return self.__activeShowtimes

    @replicated
    def removeShowtime(self, showtimeID: int):
        self.__activeShowtimes.pop(showtimeID)
        return self.__activeShowtimes

    def getShowtimes(self):
        return self.__activeShowtimes

    @replicated
    def reserveSeat(self, key: str, value: dict[str, int]):
        return

    def getSeats(self, showtimeID: int):
        return