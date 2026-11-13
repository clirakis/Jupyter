# ####################################################################
# TD_Bloch_Tx.py
#
# An effort to generate a series of points on the Bloch sphere
# and send them to another program - E.G. MAX/MSP
# for rendering.
#
# Modified   By   Reason
# --------   --   ------
# 05-Nov-26  CBL  Original
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

class TD_Bloch:
    def __init__(self):
        self.client = SimpleUDPClient("127.0.0.1", 9001)

    def Theta(self, val):
        self.client.send_message("/bloch/Theta",val)

    def Phi(self, val):
        self.client.send_message("/bloch/Phi",val)

    def __del(self):
        self.client.close()

def LoopTest():
    mine = TD_Bloch()
    theta = 0.0
    phi  = 0.0
    for i in range(5):
        mine.Theta(theta)
        theta = theta + 5.0
        for j in range(5):
            mine.Phi(phi)
            phi = phi + 10.0
        time.sleep(1)

def Test2():
    mine = TD_Bloch()
    theta = 45.0
    phi  = 0.0
    for i in range(5):
        mine.Theta(theta)
        #theta = theta + 5.0
        for j in range(5):
            mine.Phi(phi)
            phi = phi + 10.0
        time.sleep(1)

def ThetaTest():
    mine = TD_Bloch()
    theta = 0.0
    phi  = 0.0
    mine.Phi(phi)
    for i in range(19):
        print(theta)
        mine.Theta(theta)
        theta = theta + 10.0
        time.sleep(1)

def PhiTest():
    mine = TD_Bloch()
    theta = 0.0
    phi  = 0.0
    mine.Theta(90.0)
    for i in range(37):
        print(phi)
        mine.Phi(phi)
        phi = phi + 10.0
        time.sleep(1)
    
if __name__ == '__main__':
    PhiTest()
