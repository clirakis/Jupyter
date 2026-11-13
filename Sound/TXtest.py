# imports
import numpy as np
from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient
import time


def Tx():
    print('Start transmit test.')
    clientTx = SimpleUDPClient("127.0.0.1", 9002)
    for i in range(5):
        clientTx.send_message("/QRNG", i)
        time.sleep(1)
    clientTx.send_message("/Halt",0)
    print('Transmit test complete.')

if __name__ == '__main__':
    Tx()
