from reservation_manager import ReservationManager
import json
import pickle
import builtins
import time
import builtins


def print_seat_map(seats: dict):
    # Let's define rows and columns
    rows = ["a", "b", "c", "d"]
    cols = [1, 2, 3, 4, 5, 6]

    # Upper row numbers
    print("  ", end="")
    for c in cols:
        print(f"  {c}", end="")
    print()

    # The actual places
    for row in rows:
        row_label = row  
        print(f"{row_label}  ", end="")

        for col in cols:
            key = f"{row}{col}" # e.g. "a1"
            value = seats.get(key)
            ch = " " if value is None else "x"
            print(f"[{ch}]", end="")

        print('')

def seat_map_changed(node):
    if not node.getFullState()[1]:
        return

    print()
    print('The seat map has been updated:')
    print_seat_map(node.getFullState()[1])
    print()
    print("Reserve a seat by entering a seat name (e.g. a1)")

def run_console(node: ReservationManager, selfId: int):
    def print(*args, **kwargs):
        prefix = f'[N{selfId}] ' # 'N' for 'Node'

        sep = kwargs.get('sep', ' ')

        if args:
            builtins.print(prefix, end='')
            builtins.print(*args, **kwargs)
        else: # print() outputs an empty line without the prefix
            builtins.print(**kwargs)

    print('--- Welcome to the Interactive Console! ---')
    time.sleep(0.1)
    print_seat_map(node.getFullState()[1])
    print()
    print("Reserve a seat by entering a seat name (e.g. a1)")

    while True:
        userInput = input().strip().lower()
        response = node.reserveSeat(1, seatID=userInput, userID=1234, sync=True)
        continue

        print(f'\n{response["message"]}')
        if response['success']:
            commandGlobal = 'cancel' # to return to user menu
            break
        #print(render_seat_map(node.getFullState()))
        commandGlobal = '' # this is used to exit nested loops after 'cancel' or successful operation
        print()
        print('--- COMMANDS ---\nadmin\nreserve-seat\ncancel-seat\nget-showtimes\nget-state\nget-raw-logs (BROKEN)\nget-logs (BROKEN)\nget-node-status\nexit')
        print()
        print('Enter a command:')
        try:
            command = input().strip().lower()


            if command == 'admin':
                while True:
                    print()
                    print('--- ADMIN COMMANDS ---\nadd-showtime\nremove-showtime\nreturn\nexit')
                    print()
                    print('Enter a command:')
                    command = input().strip().lower()

                    if command == 'add-showtime':
                        while True:
                            print()
                            print('Enter showtimeID to add: (int | "cancel")')
                            adminInput = input().strip().lower()
                            if adminInput == 'cancel':
                                print('Operation canceled.')
                                break
                            try:
                                showtimeID = int(adminInput)
                                existingShowtimes = node.getShowtimes() 
                                if showtimeID not in list(existingShowtimes): # this line simulates an application server in the sense that identical verification is also later executed by reservation_manager.py
                                    while True:
                                        print()
                                        print('Enter theater rows: (list[dict[str, int]] | "return" | "cancel") (you can copy-paste from db.json)')
                                        adminInput = input().strip().lower()
                                        if adminInput == 'cancel':
                                            print('Operation canceled.')
                                            commandGlobal = 'cancel'
                                            break
                                        elif adminInput == 'return':
                                            break
                                        try:
                                            rows = json.loads(adminInput)
                                            response = node.addShowtime(showtimeID, rows, sync=True)
                                            print(f'{response["message"]}')
                                            if response['success']:
                                                commandGlobal = 'cancel' # to return to admin menu
                                                break
                                        except json.JSONDecodeError:
                                            print('Invalid input.')
                                        except Exception as e:
                                            print(f'Error: {type(e).__name__}: {e}')
                                else:
                                    raise ValueError(f'ERROR: Showtime with id {showtimeID} already exists.')
                            except ValueError as e:
                                print(f'Invalid input. {e}')
                                print()
                            if commandGlobal == 'cancel': # canceled after entering showtimeID --> return to admin menu
                                commandGlobal = ''
                                break

                    if command == 'remove-showtime':
                        while True:
                            showTimes = node.getShowtimes() 
                            print()
                            print(f'Showtimes in the state: {showTimes}')
                            print('Enter showtimeID to remove: (int | "cancel")')
                            adminInput = input().strip().lower()
                            if adminInput == 'cancel':
                                print('Operation canceled.')
                                break
                            try:
                                showtimeID = int(adminInput)
                                response = node.removeShowtime(showtimeID, sync=True)
                                print(f'{response["message"]}')
                                if response['success']:
                                    break
                            except ValueError as e:
                                print(f'Invalid input. {e}')

                    if command == 'return':
                        break

                    if command == 'exit':
                        commandGlobal = 'exit'
                        break


            if command == "reserve-seat":
                while True:
                    print()
                    print('Who is reserving? Enter userID: (int | "cancel")')
                    userInput = input().strip().lower()
                    if userInput == 'cancel':
                        print('Operation canceled.')
                        break
                    try:
                        userID = int(userInput)
                        while True:
                            availableShowtimes = node.getShowtimes()
                            print()
                            print(f'Available showtimes: {availableShowtimes}')
                            print('Select showtime: (int | "return" | "cancel")')
                            userInput = input().strip().lower()
                            if userInput == 'cancel':
                                print('Operation canceled.')
                                commandGlobal = 'cancel'
                                break
                            elif userInput == 'return':
                                break
                            try:
                                showtimeID = int(userInput)
                                if showtimeID in availableShowtimes:
                                    while True:
                                        availableSeats = node.getAvailableSeats(showtimeID)
                                        print()
                                        print(f'Available seats for showtime {showtimeID}: {availableSeats}')
                                        print('Select seat: (str | "return" | "cancel")')
                                        userInput = input().strip().lower()
                                        if userInput == 'cancel':
                                            print('Operation canceled.')
                                            commandGlobal = 'cancel'
                                            break
                                        elif userInput == 'return':
                                            break
                                        try:      
                                            response = node.reserveSeat(showtimeID, seatID=userInput, userID=userID, sync=True)
                                            print(f'{response["message"]}')
                                            if response['success']:
                                                commandGlobal = 'cancel' # to return to user menu
                                                break
                                        except Exception as e:
                                            print(f'Error: {type(e).__name__}: {e}')
                                else:
                                    print('Please select a showtime that exists in the state.')
                            except ValueError as e:
                                print(f'Invalid input. {e}')
                            if commandGlobal == 'cancel': # canceled after entering showtimeID --> return to user menu
                                break # commandGlobal not edited because there is one more outer loop to exit
                    except ValueError:
                        print('Invalid input.')
                    if commandGlobal == 'cancel': # canceled or success after entering userID --> return to user menu
                        commandGlobal = ''
                        break
            
            if command == 'cancel-seat':
                while True:
                    availableShowtimes = node.getShowtimes()
                    print()
                    print(f'Showtimes in the state: {availableShowtimes}')
                    print('Select showtime to cancel a seat from: (int | "cancel")')
                    userInput = input().strip().lower()
                    if userInput == 'cancel':
                        print('Operation canceled.')
                        commandGlobal = 'cancel'
                        break
                    try:
                        showtimeID = int(userInput)
                        if showtimeID in availableShowtimes:
                            while True:
                                reservedSeats = node.getReservedSeats(showtimeID)
                                print()
                                print(f'Reserved seats for showtime {showtimeID}: {reservedSeats}')
                                print('Select a seat to cancel: (str | "return" | "cancel")')
                                userInput = input().strip().lower()
                                if userInput == 'cancel':
                                    print('Operation canceled.')
                                    commandGlobal = 'cancel'
                                    break
                                elif userInput == 'return':
                                    break
                                try:      
                                    response = node.cancelSeat(showtimeID, seatID=userInput, sync=True)
                                    print(f'{response["message"]}')
                                    if response['success']:
                                        commandGlobal = 'cancel' # to return to user menu
                                        break
                                except Exception as e:
                                    print(f'Error: {type(e).__name__}: {e}')
                        else: 
                            print('Please select a showtime that exists in the state.')
                    except ValueError as e:
                        print(f'Invalid input. {e}')
                    if commandGlobal == 'cancel': # canceled or success after entering showtimeID --> return to user menu
                        commandGlobal = ''
                        break

            elif command == 'get-showtimes':
                showTimes = node.getShowtimes()
                print(f'Showtimes: {showTimes}')

            elif command == 'get-state':
                all = node.getFullState()
                print(all)

            elif command == 'get-raw-logs':
                raw_logs = node.getLogs()
                for log in raw_logs:
                    print(log)

            elif command == 'get-logs':
                FUNCTION_MAP = {
                    0: 'addShowtime',
                    3: 'reserveSeat'
                    # TODO: Add other functions from reservation_manager.py. Note that the mapping above might be incorrect since the functions in reservation_manager.py have been reordered.
                }

                raw_log = node.getLogs()
                print()
                print(f"{'INDEX':<5} | {'TERM':<5} | {'DATA'}")
                print("-" * 40)

                for entry in raw_log:
                    binary_data, index, term = entry

                    if binary_data == b'\x01':
                        decoded_data = '[Internal] No-Op / Heartbeat'
                    
                    elif binary_data.startswith(b'\x00'):
                        try:
                            decoded_data = pickle.loads(binary_data[1:]) # decoded_data is a 3-tuple
                            function_name = FUNCTION_MAP.get(decoded_data[0], f'Unknown_ID_{decoded_data[0]}')
                            if function_name == 'addShowtime': 
                                decoded_data = f'{function_name}{decoded_data[1]}' # addShowtime has the arguments in decoded_data[1]
                            elif function_name == 'reserveSeat':
                                decoded_data = f'{function_name}({decoded_data[2]})' # reserveSeat has the arguments in decoded_data[2]
                            else:
                                decoded_data = f'{function_name}({decoded_data[1]})({decoded_data[2]})'
                        except Exception as e:
                            decoded_data = f'<Corrupt Data: {e}>'
                    
                    else:
                        decoded_data = f'<Unknown Binary: {binary_data[:10]}...>'

                    print(f'{index:<5} | {term:<5} | {decoded_data}')
        
            elif command == 'get-node-status':
                status = node.getCustomStatus()
                print()
                print(status)

            elif command == 'exit' or commandGlobal == 'exit': # the latter activated when admin exits
                print("Exiting.")
                break
        
            elif command == 'return' or command == 'reserve-seat':
                # catch exits from inner loops
                continue

            elif command:
                print(f'Unknown command: "{command}"')

        except KeyboardInterrupt:
            print("Exiting on interrupt.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def render_seat_map(rows: dict[str, dict[str, object]]) -> None:
    # rows = { "A": {"A1": None, "A2": 123, ...}, "B": {...}, ... }
    def seat_key(seat_id: str) -> int:
        # lajittelee A1, A2, A10 numeron mukaan
        num = ''.join(ch for ch in seat_id if ch.isdigit())
        return int(num) if num else 0

    for row_label in sorted(rows.keys()):  # rivit aakkosjärjestyksessä
        seats = rows[row_label]
        line = [row_label]  # rivin tunnus alkuun
        for seat_id in sorted(seats.keys(), key=seat_key):
            value = seats[seat_id]
            reserved = bool(value)  # True/uid => varattu, None/False/0/"" => vapaa
            line.append('[x]' if reserved else '[ ]')
        print(' '.join(line))





