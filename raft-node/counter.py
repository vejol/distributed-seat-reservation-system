#!/usr/bin/env python
import sys
import time
from functools import partial
sys.path.append("../")
from pysyncobj import SyncObj, replicated

class MyCounter(SyncObj):
    def __init__(self, selfNodeAddr, otherNodeAddrs):
        super(MyCounter, self).__init__(selfNodeAddr, otherNodeAddrs)
        self.__counter = 0

    @replicated
    def incCounter(self):
        self.__counter += 1
        return self.__counter

    @replicated
    def addValue(self, value, cn):
        self.__counter += value
        return self.__counter, cn

    def getCounter(self):
        return self.__counter


def onAdd(res, err, cnt):
    print('onAdd %d:' % cnt, res, err)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: %s self_port partner1_port partner2_port ...' % sys.argv[0])
        sys.exit(-1)

    port = int(sys.argv[1])
    partners = ['localhost:%d' % int(p) for p in sys.argv[2:]]
    node = MyCounter('localhost:%d' % port, partners)

    while True:
        try:
            # allow the cluster time to stabilise
            time.sleep(0.5)

            command = input().strip().lower()

            if command == 'inc':
                node.incCounter()
                print('Replication call sent.')
            
            elif command == 'add':
                print('Not implemented!')
            
            elif command == 'get':
                value = node.getCounter()
                print(f'Currect local counter value: {value}')
            
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
    