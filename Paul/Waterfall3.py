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

class WaterFall():
    """
    This is a nice way to encapsulate data such that it won't be
    overwritten or munged in any way. 
    """
    def __init__(self, Upper_Frequency, Upper_Time):
        """Initialize the Waterfall display. 
        @param Upper_Frequency (integer) - maximum frequeny to be displayed.
        @param Upper_Time (integer) - size of window to display
        """
        # Create a window to display the waterfall inside of.
        # replace here if embedded in larger context. 
        self.fig,self.ax = plt.subplots()
        #
        # Make a 2D array to make the image.
        # currently agnostic on axis and binsize is defaulted to 1. 
        #
        Data2D = np.zeros((Upper_Frequency, Upper_Time), dtype=float)
        self.img = self.ax.imshow(Data2D)
        self.fig.colorbar(self.img, ax=self.ax, label="test plot")

    def __str__(self):
        """str function to aid in printing out characteristics.
        No inputs other than self. 
        """
        data = self.img.get_array()
        return f"Waterfall, Frequency Bins: '{data.shape[0]}', Time Window: '{data.shape[1]}'"
        
    def Update(self, frame):    
        """Update the plot as necessary.
        @param frame - needs to be defined in the context of the usage. 
        """
        # some call or function
        # get a handle to the original data set.
        data = self.img.get_array()
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
        self.img.set_array(data)
        

def update(frame, farg):
    """ update the data within the waterfall.
    This is a callback function, as such the input parameters have
    a very specific layout.
    reference:
    https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html
    https://matplotlib.org/stable/users/explain/animations/animations.html
    
    @param frame - count on the number of times the update function
            has been called.
    @param farg - arguments passed in. 
    """
    #print (farg)
    farg.Update(frame)
    # needed comma in return to make blit=True work!
    return farg.img,
   
if __name__ == "__main__":
    MaxFreq = 100      # number frequency bins
    MaxTime = 100      # number of time sweeps.
    #
    # instantiate the class.
    wf = WaterFall(MaxFreq,MaxTime)

    ani = anim.FuncAnimation(wf.fig, update, fargs=(wf,), frames=range(100),
                             interval=250, blit=True)
    plt.show()
