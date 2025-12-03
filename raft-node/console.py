from reservation_manager import ReservationManager
import json
import pickle

def run_console(node: ReservationManager):
    print('\n--- Welcome to the Interactive Console! ---')

    while True:
        commandGlobal = '' # this is used to exit nested loops after 'cancel' or successful operation
        print('\n--- COMMANDS ---\nadmin\nreserve-seat\ncancel-seat (not implemented)\nget-showtimes\nget-full-state\nget-raw-logs\nget-logs (BETA)\nget-status\nexit\n')
        print('Enter a command:')
        try:
            command = input().strip().lower()

            if command == 'admin':
                while True:
                    print('\n--- ADMIN COMMANDS ---\nadd-showtime\nremove-showtime (not implemented)\nreturn\nexit\n')
                    print('Enter a command:')
                    command = input().strip().lower()
                    if command == 'add-showtime':
                        while True:
                            print('\nEnter showtimeID: (int | "cancel")')
                            adminInput = input().strip().lower()
                            if adminInput == 'cancel':
                                print('Operation canceled.')
                                break
                            try:
                                showtimeID = int(adminInput)
                                existingShowtimes = node.getShowtimes() 
                                if showtimeID not in list(existingShowtimes): # this line simulates an application server in the sense that identical verification is also later executed by reservation_manager.py
                                    while True:
                                        print('\nEnter theater rows: (list[dict[str, int]] | "return" | "cancel") (you can copy-paste from db.json)')
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
                                            print(f'\n{response["message"]}')
                                            if response['success']:
                                                commandGlobal = 'cancel' # to return to admin menu
                                                break
                                        except json.JSONDecodeError:
                                            print('Invalid input.')
                                        except Exception as e:
                                            print(f'Error: {type(e).__name__}: {e}')
                                else:
                                    raise ValueError(f'\nERROR: Showtime with id {showtimeID} already exists.\n')
                            except ValueError as e:
                                print(f'Invalid input.{e}')
                            if commandGlobal == 'cancel': # canceled after entering showtimeID --> return to admin menu
                                commandGlobal = ''
                                break

                    if command == 'remove-showtime':
                        print(f'Oh no! This command is not implemented, yet.')

                    if command == 'return':
                        break

                    if command == 'exit':
                        commandGlobal = 'exit'
                        break


            if command == "reserve-seat":
                while True:
                    print('\nWho is reserving? Enter userID: (int | "cancel")')
                    userInput = input().strip().lower()
                    if userInput == 'cancel':
                        print('Operation canceled.')
                        break
                    try:
                        userID = int(userInput)
                        while True:
                            availableShowtimes = node.getShowtimes()
                            print(f'\nAvailable showtimes: {availableShowtimes}')
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
                                        print(f'\nAvailable seats for showtime {showtimeID}: {availableSeats}')
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
                                            print(f'\n{response["message"]}')
                                            if response['success']:
                                                commandGlobal = 'cancel' # to return to user menu
                                                break
                                        except Exception as e:
                                            print(f'Error: {type(e).__name__}: {e}')
                                else:
                                    print('Invalid input.')
                            except ValueError:
                                print('Invalid input.')
                            if commandGlobal == 'cancel': # canceled after entering showtimeID --> return to user menu
                                break # commandGlobal not edited because there is one more outer loop to exit
                    except ValueError:
                        print('Invalid input.')
                    if commandGlobal == 'cancel': # canceled after entering userID --> return to user menu
                        commandGlobal = ''
                        break
            
            if command == 'cancel-seat':
                print(f'Oh no! This command is not implemented, yet.')

            elif command == 'get-showtimes':
                showTimes = node.getShowtimes()
                print(showTimes)

            elif command == 'get-full-state':
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
                    # TODO: Add other functions from reservation_manage.py
                }

                raw_log = node.getLogs()
                print(f"{'IDX':<5} | {'TERM':<5} | {'DATA'}")
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
        
            elif command == 'get-status':
                status = node.getCustomStatus()
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
            print("\nExiting on interrupt.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
