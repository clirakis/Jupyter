# ####################################################################
# BlochSphere.py
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

client = udp_client.SimpleUDPClient("127.0.0.1", 9001)

def set_phase(address,phi):
    x = float(np.cos(phi))
    y = float(np.sin(phi))
    z = 0.0
    print (f"phi={phi:.3f} x={x:.3f} y={y:.3f} z={z:.3f}")
    client.send_message("/bloch/state, [x, y, z]")


dispatch = dispatcher.Dispather()
dispatch.map("/qubit/phase", set_phase)
server = osc_server.ThreadingOSCUDPServer(
    ("127.0.0.1", 9000), dispatch
)
print ("Listening for OSC on port 9000")
server.serve_forever()
