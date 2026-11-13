"""
documentation
https://python-osc.readthedocs.io/en/stable/server.html
may want to use asyncio example
"""
# imports
import numpy as np
from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import time
import threading

ThreadRun = True

def EventHandler(address, *args):
    global ThreadRun
    global server
    print(f"Received: {address}, Arguments: {args}")
    if address == "/Halt":
        print('Halt received.')
        ThreadRun = False
        server.shutdown()

def Rx():
    print('Start recieve test.')
    clientRx = SimpleUDPClient("127.0.0.1", 9002)
    msgs = clientRx.get_messages(10)
    for m in msgs:
        print(m.address)

    print('Recieve test complete.')

def BlockingServer():
    global server
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(EventHandler)
    # lisetn on local host.
    server = BlockingOSCUDPServer(("127.0.0.1", 9002), dispatcher)
    print("Listening on port 9002")
    server.serve_forever()


def ThreadedBlock():
    global ThreadRun
    global server
    dispatcher = Dispatcher()
    dispatcher.set_default_handler(EventHandler)
    # lisetn on local host.
    server = BlockingOSCUDPServer(("127.0.0.1", 9002), dispatcher)
    print("Listening on port 9002")
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    print("Server thread started.")
    i = 0
    while(ThreadRun):
        print(i, ", ", ThreadRun)
        i = i + 1
        time.sleep(1)
    server.shutdown()
    server.server_close()
    server_thread.join()
    print('Closeout.')
    
    
if __name__ == '__main__':
    BlockingServer()
    #print('Creating thread.')
    #t1 = threading.Thread(target="BlockingServer")
    #print('starting thread')
    #t1.start()
    #print('waiting for thread to terminate')
    #t1.join()
    #ThreadedBlock()
    print('program ends')
