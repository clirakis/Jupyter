"""
 ####################################################################
  RxTxOSC.py

  Communication protocol to send them to another program - E.G. MAX/MSP
  for rendering.

  Modified   By   Reason
  --------   --   ------
  12-Nov-26  CBL  Original

  References:
  OSC/UDP interface 
     https://docs.cycling74.com/legacy/max5/refpages/max-ref/udpreceive.html
     https://python-osc.readthedocs.io/en/latest/"
     https://python-osc.readthedocs.io/en/latest/client.html#module-pythonosc.udp_client"

  Make sure you have the python interface

     pip install python_osc  
  
  Notes:
      https://python-osc.readthedocs.io/en/stable/server.html
      may want to use asyncio example
  ####################################################################
"""
# imports
import numpy as np
from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import time
import threading

# Local includes
from TxOSC import TxOSC

# Global variable. May not need. 
ThreadRun = True
iFreq = 110.0

def Halt(address, *args):
    """
    Shutdown this server
    """
    print('HALT!')
    global server
    ThreadRun = False
    threading.Thread(target=server.shutdown, daemon=True).start()

def Gimme(address, *args):
    """
    example of a general request. 
    """
    global Tx
    global iFreq
    Tx.FreqPhase(iFreq, 0.0)
    iFreq = iFreq * 2
    
def EventHandler(address, *args):
    """
    This is the callback function for the dispatcher.
    For each UDP packet received, it will be called.
    My intent here is that this looks for the /COMMAND prefix to
    tell this program something to do. EG if it is qiskit
    give me some more samples.
    @param address - the address prefix from the OSC message
    @param *args   - this may be a list of arguments of any type. 
    """
    global Tx
    print(f"Received: {address}, Arguments: {args}")
        
def Initialize():
    """
    Initialize any other stuff here. predominatly setup the
    UDP socket for sending the data to MAX or Touch Designer.
    """
    global Tx
    # setup a client for sending messages to port 9001
    Tx = TxOSC()
    print ('Initialize')
    
def Finalize():
    """
    do any necessary cleanup on exit. 
    """
    global Tx
    del Tx
    print('Finalize')
    
def BlockingServer():
    """
    This is kind of the main call for this example. It sets up the
    Dispather and then tells it that EventHandler method from above
    is to as it says handle all the inbound events.
    
    """
    global server
    dispatcher = Dispatcher()
    dispatcher.map("/Halt", Halt)
    dispatcher.map("/Gimme", Gimme)
    dispatcher.set_default_handler(EventHandler)
    # lisetn on local host. The receive port for this process
    # is 9002. 
    server = BlockingOSCUDPServer(("127.0.0.1", 9002), dispatcher)
    print("Listening on port 9002")
    # Not yet sure how this exits. It will as it says do an endless loop
    # This can be moved into its own thread to make a loop here if
    # we want. 
    server.serve_forever()
    
    
if __name__ == '__main__':
    Initialize()
    BlockingServer()
    print('program ends')
    Finalize()
