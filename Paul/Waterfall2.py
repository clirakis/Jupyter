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

Matplotlib examples:
https://matplotlib.org/stable/gallery/index.html

Animation:


"""
# Standard imports
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anim
import time

# These are handy, but may not be needed in this example. 
import math
import scipy.constants as const

# Global Variables, I am not a big fan of this.
# This does make sure that they exist.
# this should be hidden in a class. 
img         = []

def MakeWaterFall(MaxFreq, TimeWindow=10):
    """ Make a waterfall display
    @param MaxFreq - maximum frequeny to be displayed.
    @param TimeWindow - size of window to display
    """
    fig,ax = plt.subplots()
    #
    # create a new line array for data.
    #
    new_line = np.zeros(TimeWindow)
    #
    # Make a 2D array to make the image.
    # currently agnostic on axis and binsize is defaulted to 1. 
    #
    Data2D = np.zeros((MaxFreq, TimeWindow), dtype=float)
    img = ax.imshow(Data2D)
    fig.colorbar(img, ax=ax, label="test plot")
    #plt.show(animated=True)
    return fig, img

def update(frame):
    """ update the data within the waterfall.
    This is a callback function.
    """
    # get a handle to the original data set.
    data = img.get_array()
    # need another method of getting the new data into the system
    # this is an example only. 
    max = 2.0*const.pi
    # give me a frequency range. 
    omega = np.arange(0, max, max/data.shape[0])
    # increment the phase to make it interesting.
    phase = frame * const.pi/20
    new_line = np.sin(omega+phase)

    # update the data
    data[frame,] = new_line
    # You can attach this to the D/A for the instrument in one of two
    # ways, either just call it here, or create a thread and use
    # a semaphore to block this until the data is ready.
    # Since Ed just learned about tkinter widgets he can embed this
    # into a frame. I prefer WxWidgets
    # update the data in the image. 
    img.set_array(data)
    # needed comma in return to make blit=True work!
    return img,
   
if __name__ == "__main__":
    MaxFreq = 100      # number frequency bins
    MaxTime = 100      # number of time sweeps.
    #
    fig, img = MakeWaterFall(MaxFreq,MaxTime)

    ani = anim.FuncAnimation(fig, update, frames=range(100), interval=250,
                                  blit=True)
    plt.show()
