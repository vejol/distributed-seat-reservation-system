from reservation_manager import ReservationManager
import json

def run_console(node: ReservationManager):
    print('\n--- Welcome to the Interactive Console! ---\n')

    while True:
        print('Commands:\nadmin\nreserve-seat (not implemented)\ncancel-seat (not implemented)\nget-showtimes\nexit')
        try:
            command = input().strip().lower()

            if command == 'admin':
                while True:
                    print('Admin Commands\nadd-showtime\nremove-showtime (not implemented)\nexit-admin')
                    command = input().strip().lower()
                    if command == 'add-showtime':
                        while True:
                            print('Enter showtimeID (int | "cancel")')
                            adminInput = input().strip().lower()
                            if adminInput.lower() == 'cancel':
                                print('Operation canceled.')
                                break
                            try:
                                showtimeID = int(adminInput)
                                print('Enter theater rows (list[dict[str, int]] | "cancel") (you can copy-paste from db.json)')
                                adminInput = input().strip().lower()
                                if adminInput.lower() == 'cancel':
                                    print('Operation canceled.')
                                    break
                                try:
                                    rows = json.loads(adminInput)
                                    node.addShowtime(showtimeID, rows)
                                    print('Showtime added successfully.')
                                except json.JSONDecodeError:
                                    print('Invalid input.')
                                break
                            except ValueError:
                                print('Invalid input.')

                    if command == 'remove-showtime':
                        print(f'Oh no! This command is not implemented, yet.')

                    if command == 'exit-admin':
                        break


            if command == "reserve-seat":
                print(f'Oh no! This command is not implemented, yet.')
            
            if command == "cancel-seat":
                print(f'Oh no! This command is not implemented, yet.')

            elif command == 'get-showtimes':
                value = node.getShowtimes()
                print(value)

            elif command == 'exit':
                print("Exiting.")
                break
        
            elif command == 'exit-admin':
                # configure this inside the admin loop
                continue

            elif command:
                print(f'Unknown command: "{command}"')

        except KeyboardInterrupt:
            print("\nExiting on interrupt.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
