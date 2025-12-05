from pathlib import Path
from pysyncobj import SyncObj, SyncObjConf, replicated
from typing import TypedDict

ActiveShowtimes = dict[int, dict[str, int]] # { showtimeID: { seatID: userID, seatID: userID ... } } 
# available seats have userID = None
TheaterRows = TypedDict('TheaterRows', {'row': str, 'seats': int})
# used in addShowTime, something for Application Servers to mind

class ReservationManager(SyncObj):
    def __init__(self, selfNodeAddr, otherNodeAddrs, on_seat_map_changed):

        conf = SyncObjConf(
            journalFile=self._generateUniqueFileName("journal", selfNodeAddr),
            fullDumpFile=self._generateUniqueFileName("dump", selfNodeAddr),
            logCompactionMinTime=60,  # take snapshot in every 60 seconds
            logCompactionMinEntries=5,  # take snapshot in every 5 entries
        )

        super(ReservationManager, self).__init__(selfNodeAddr, otherNodeAddrs, conf)
        self.__activeShowtimes: ActiveShowtimes = {
            1: {'a1': None, 'a2': None, 'a3': None, 'a4': None, 'a5': None, 'a6': None, 'b1': None, 'b2': None, 'b3': None, 'b4': None, 'b5': None, 'b6': None, 'c1': None, 'c2': None, 'c3': None, 'c4': None, 'c5': None, 'c6': None, 'd1': None, 'd2': None, 'd3': None, 'd4': None, 'd5': None, 'd6': None}
        }
        self._on_seat_map_changed = on_seat_map_changed

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
        self._on_seat_map_changed(self)

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

    def getLogs(self):
        return self._SyncObj__raftLog._MemoryJournal__journal
    
    # Adapted from getStatus(). See syncobj.py from the source code for details (or look below). Explanations from Ongaro & Ousterhout, 2014.
    def getCustomStatus(self):
        status = {}
        status['self'] = self.selfNode
        status['state'] = self._SyncObj__raftState
        status['leader'] = self._SyncObj__raftLeader
        status['has_quorum'] = self.hasQuorum
        status['partner_nodes'] = self._SyncObj__otherNodes
        status['partner_nodes_count'] = len(self._SyncObj__otherNodes)
        status['raft_term'] = self.raftCurrentTerm # latest term server has seen
        status['commit_idx'] = self.raftCommitIndex # index of highest log entry known to be committed
        status['last_applied'] = self.raftLastApplied # index of highest log entry applied to state machine
        for node, idx in self._SyncObj__raftNextIndex.items():
            status['next_node_idx_server_' + node.id] = idx # for each server, index of the next log entry to send to that server
        for node, idx in self._SyncObj__raftMatchIndex.items():
            status['match_idx_server_' + node.id] = idx # for each server, index of highest log entry known to be replicated on server
        status['leader_commit_idx'] = self._SyncObj__leaderCommitIndex # FOLLOWERS: If leader_commit_idx > commit_idx, set commit_idx min(leader_commit_idx, index of last new entry)
        return(status)
    


    
    @replicated
    def removeShowtime(self, showtimeID: int):
        #TODO add error handling
        self.__activeShowtimes.pop(showtimeID)
        return self.__activeShowtimes
    
    def getAvailableShowtimes(self):
        # TODO this should return showtimes that have at least one free seat
        return
    
    @replicated
    def cancelSeat(self):
        # TODO
        return

    def getSeats(self, showtimeID: int):
        # TODO
        return
    
    # Every node needs unique file names for journal and dump files.
    # The id parameter is unique identifier of node. For example "localhost:6000"
    # The keyword parameter describes the first word of the filename. For example "journal"
    def _generateUniqueFileName(self, keyword, id):
        path = Path(__file__).resolve().parent / "journal"
        path.mkdir(parents=True, exist_ok=True)
        safe_id = id.replace(":", "_")
        return str(path / f"{keyword}-{safe_id}.bin")
    
# DEV NOTE: you can copy-paste the line below (taken from db.json) when using addShowtime
# [{"row": "A","seats": 2},{"row": "B","seats": 2}]

# self.__raftLog returns logs as a list

# getStatus() from source code for reference
""" def getStatus(self):
    status = {}
    status['version'] = VERSION
    status['revision'] = 'deprecated'
    status['self'] = self.selfNode
    status['state'] = self.__raftState
    status['leader'] = self.__raftLeader
    status['has_quorum'] = self.hasQuorum
    status['partner_nodes_count'] = len(self.__otherNodes)
    for node in self.__otherNodes:
        status['partner_node_status_server_' + node.id] = 2 if self.isNodeConnected(node) else 0
    status['readonly_nodes_count'] = len(self.__readonlyNodes)
    for node in self.__readonlyNodes:
        status['readonly_node_status_server_' + node.id] = 2 if self.isNodeConnected(node) else 0
    status['log_len'] = len(self.__raftLog)
    status['last_applied'] = self.raftLastApplied
    status['commit_idx'] = self.raftCommitIndex
    status['raft_term'] = self.raftCurrentTerm
    status['next_node_idx_count'] = len(self.__raftNextIndex)
    for node, idx in iteritems(self.__raftNextIndex):
        status['next_node_idx_server_' + node.id] = idx
    status['match_idx_count'] = len(self.__raftMatchIndex)
    for node, idx in iteritems(self.__raftMatchIndex):
        status['match_idx_server_' + node.id] = idx
    status['leader_commit_idx'] = self.__leaderCommitIndex
    status['uptime'] = int(monotonicTime() - self.__startTime)
    status['self_code_version'] = self.__selfCodeVersion
    status['enabled_code_version'] = self.__enabledCodeVersion
    return status """