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

  ####################################################################
"""
# imports
import numpy as np
from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient
import time

"""
Class to manage the OSC exchange

I've got several things I'm setting up here. The method generic send,
just sends over the random number without any prefix other than /QRNG.
You can kind of see how I'm building a larger vocabulary here.
There is a decision by the artist that needs to be made, where are
you going to do the heavy lifting, here or in the consumer
(MAX/MSP or Touch Designer or any other OSC consumer.) My preference is
here since I'm very comfortable with Python and Jupyter.
I will build in an event loop that is just here AND I will also setup a
way to accept messages from the OSC consumer.

Simple Vocabulary:

/OSCnumber [Frequency, Phase] - send a frequency phase pair to the oscillator number.
/QRNG value - just send a raw random number.
There is a companion set of patches, programs or whatever is the name that go with this. The MAX/MSP one is called UDP5 and has examples of how I parse the messages.
"""
class OSC_RxTx:
    """
    Very simple wrapper for OSC exchange. 
    Message content is very simple. Choosing to potentially have multiple oscillators and other controllers. 
    The OSC address string is therefore OBJECT INSTANCE
    """
    def __init__(self):
        """
        MAX/MSP or Touch Designer is the server. We are the client. It is kind of a coin toss as to which is
        which but I decided this makes the most sense to me. I've hard coded the address to localhost
        and the port to 9001. Change at your leisure. 
        """
        self.clientTx = SimpleUDPClient("127.0.0.1", 9001)
        self.clientRx = SimpleUDPClient("127.0.0.1", 9002)

    def GenericSend(self, val):
        """
        Just send a value over, let the receiving program do the heavy lifting. 
        """
        self.clientTx.send_message("/QRNG", val)

    def FreqPhase(self, f=440.0, phi=0.0, osc=1):
        """
        Send Frequency phase pair. 
        @param f - frequency
        @param phi - phase
        """
        to_send = "/osc/"+str(osc)
        self.clientTx.send_message(to_send,[f,phi])

     def Commands(self):
        """
        Check to see if there are any messages to us from the server. 
        The argument on get messages is the timeout for waiting for an 
        inbound message. The caller is responsible for checking that
        there is a message of value. 
        """
        messages = self.clientRx.get_messages(2)
        
        #for msg in messages:
        #    print("Address: ", msg.address, " Data: ", msg.params)
        print(dir(messages))
       
    def __del(self):
        """
        Do any clean up when we are done. 
        """
        self.client.close()
