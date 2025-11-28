from reservation_manager import ReservationManager


def run_console(node: ReservationManager):
    print("\n--- Interactive Console ---")
    print("Commands: **reserve**, **get**, **exit**")  # TODO: implement **cancel**

    while True:
        try:
            command = input().strip().lower()

            if command == "reserve":
                print('Who is reserving? (enter a name or write "exit")')
                userName = input().strip()
                if userName.lower() == "exit":
                    print("Seat reservation canceled. Enter next command.")
                else:
                    print(
                        'Which seat would you like to book? (enter a seat number or write "exit")'
                    )
                    while True:
                        userInput = input().strip()
                        if userInput.lower() == "exit":
                            print("Seat reservation canceled. Enter next command.")
                            break
                        try:
                            val = int(userInput)
                            node.reserveSeat(
                                val, {userName: 123}
                            )  # TODO: change hardcoded 123 to something meaningful
                            print(f"Seat {val} reserved!")
                            break
                        except ValueError:
                            print(
                                'Please enter a number. (enter a seat number or write "exit")'
                            )

            elif command == "get":
                value = node.getSeats()
                print(f"Reserved seats: {value}")

            elif command == "exit":
                print("Exiting.")
                break

            elif command:
                print(f'Unknown command: "{command}"')

        except KeyboardInterrupt:
            print("\nExiting on interrupt.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
