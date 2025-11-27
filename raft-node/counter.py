#!/usr/bin/env python
import sys
import time
from functools import partial
sys.path.append("../")
from pysyncobj import SyncObj, replicated

ReservedSeats = dict[int, dict[str, int]] 
#TODO: change key to str

class MyCounter(SyncObj):
    def __init__(self, selfNodeAddr, otherNodeAddrs):
        super(MyCounter, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.__reservedSeats: ReservedSeats = {
            # example: 1: { "user": 123 }
        }

    @replicated
    def reserveSeat(self, key: str, value: dict[str, int]):
        self.__reservedSeats[key] = value
        return self.__reservedSeats

    def getSeats(self):
        return self.__reservedSeats

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: %s self_port partner1_port partner2_port ...' % sys.argv[0])
        sys.exit(-1)

    port = int(sys.argv[1])
    partners = ['localhost:%d' % int(p) for p in sys.argv[2:]]
    node = MyCounter('localhost:%d' % port, partners)

    print('\n--- Interactive Console ---')
    print('Commands: **reserve**, **get**, **exit**') # TODO: implement **cancel**

    while True:
        try:
            command = input().strip().lower()

            if command == 'reserve':
                print('Who is reserving? (enter a name or write "exit")')
                userName = input().strip()
                if userName.lower() == 'exit':
                    print('Seat reservation canceled. Enter next command.')
                else:
                    print('Which seat would you like to book? (enter a seat number or write "exit")')
                    while True:
                        userInput = input().strip()
                        if userInput.lower() == 'exit':
                            print('Seat reservation canceled. Enter next command.')
                            break
                        try:
                            val = int(userInput)
                            node.reserveSeat(val, {userName: 123}) #TODO: change hardcoded 123 to something meaningful
                            print(f'Seat {val} reserved!')
                            break
                        except ValueError:
                            print('Please enter a number. (enter a seat number or write "exit")')
            
            elif command == 'get':
                value = node.getSeats()
                print(f'Reserved seats: {value}')
            
            elif command == 'exit':
                print('Exiting.')
                break

            elif command:
                print(f'Unknown command: "{command}"')
    
        except KeyboardInterrupt:
            print('\nExiting on interrupt.')
            break
        except Exception as e:
            print(f'An error occurred: {e}')
            break
    