"""@package Waterfall.py
Waterfall.py

Modified   By   Reason
--------   --   --------
21-Jul-25  CBL  Built off Paul's code but taking a different approach.

Note: I use python env command to create python environments. It is
so easy to screw up package management that in this case you  can blow
it away without fubaring your system.

See here:
https://docs.python.org/3/library/venv.html


"""
# Standard imports
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anim
import time

# These are handy, but may not be needed in this example. 
import math
import scipy.constants as const


def MakeWaterFall(MaxFreq, TimeWindow=10):
    """ Make a waterfall display
    @param MaxFreq - maximum frequeny to be displayed.
    @param TimeWindow - size of window to display
    """
    fig,ax = plt.subplots()
    #
    # Make a 2D array to make the image.
    # currently agnostic on axis and binsize is defaulted to 1. 
    #
    Data2D = np.zeros((MaxFreq, TimeWindow), dtype=float)
    img = ax.imshow(Data2D)
    fig.colorbar(img, ax=ax, label="test plot")
    # the next call is a blocking call, unless otherwise specified. 
    plt.show(block=False)
    return img

def update(img, line_number, new_line):
    """ update the data within the waterfall.
    @param img - image of waterfall.
    @param line_number - line number to change
    @param new_line    - line of new data, length=MaxFreq. 
    """
    # get a handle to the original data set.
    data = img.get_array()
    print("Shape of retrieved data:", data.shape)
    # update the data
    data[line_number,] = new_line
    # update the data in the image. 
    img.set_array(data)
    plt.show(block=False)
    
if __name__ == "__main__":
    MaxFreq = 100      # number frequency bins
    MaxTime = 100      # number of time sweeps.
    #
    img = MakeWaterFall(MaxFreq,MaxTime) 
    max = 2.0*const.pi
    # give me a frequency range. 
    omega = np.arange(0, max, max/MaxFreq) 
    phase = 0
    # Make a loop for purposes of illustration. 
    for i in range(MaxTime):
        line = np.sin(omega+phase)
        update(img, i, line)
        #time.sleep(1.0)
        # increment the phase to make it interesting.
        phase = phase + const.pi/20
        val = input("press a key to continue.")
        if (val=='q'):
            break
