from pysyncobj import SyncObj, replicated

ReservedSeats = dict[int, dict[str, int]]
# TODO: change key to str


class ReservationManager(SyncObj):
    def __init__(self, selfNodeAddr, otherNodeAddrs):
        super(ReservationManager, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.__reservedSeats: ReservedSeats = {
            # example: 1: { "user": 123 }
        }

    @replicated
    def reserveSeat(self, key: str, value: dict[str, int]):
        self.__reservedSeats[key] = value
        return self.__reservedSeats

    def getSeats(self):
        return self.__reservedSeats
