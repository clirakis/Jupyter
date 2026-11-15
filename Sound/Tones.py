# ####################################################################
# Tones.py
#
# An effort to generate a series of sounds
# and send them to another program - E.G. MAX/MSP
# for rendering.
#
# Modified   By   Reason
# --------   --   ------
# 11-Nov-26  CBL  Original
#
# References:
#
#
# Notes:
#
#
# ####################################################################
# imports
import numpy as np
from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient
import time

class TD_Tone:
    def __init__(self):
        self.client = SimpleUDPClient("127.0.0.1", 9001)

    def Freq(self, val):
        self.client.send_message("/osc/frequency",val)

    def Phase(self, val):
        self.client.send_message("/osc/Phase",val)

    def __del(self):
        self.client.close()

def LoopTest():
    mine = TD_Tone()

    freq = 110
    for i in range(6):
        mine.Freq(freq)
        freq = freq * 2
        time.sleep(1)

def SetTone():
    mine = TD_Tone()

    freq = 110
    mine.Freq(freq)
    
    
if __name__ == '__main__':
    #SetTone()
    LoopTest()
