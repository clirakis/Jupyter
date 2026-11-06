# #####################################################################
# RNG.py
#
#
# Modification history
# Modified By  Reason
# -------- --  ------
# 05-Nov-26 CBL Original with help from Sal
#
# References 
#    
#
# Notes 
#
##
# #####################################################################
from manim import *
import numpy as np

class BlochSphere(ThreeDScene):
    def construct(self):
        """
        Camera orientation
        """
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-45 * DEGREES
            )
        axes = ThreeDAxes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            z_range=[-1.5, 1.5, 1],
            x_length=5,
            y_length=5,
            z_length=5
        )
        sphere = Sphere(
            radius=2.5,
            resolution=(24, 48)
        )
        sphere.set_fill(BLUE, opacity=0.12)
        sphere.set_stroke(BLUE, opacity=0.2)
        self.add(axes, sphere)
        # The state vector is parameterized
        # by polar angle theta and azimuth phi.
        theta = ValueTracker(0)
        phi = ValueTracker(0)
        def endpoint():
            t = theta.get_value()
            p = phi.get_value()
            return axes.c2p(
                np.sin(t) * np.cos(p),
                np.sin(t) * np.sin(p),
                np.cos(t)
            )
        vector = always_redraw(
            lambda: Arrow3D(
                start=ORIGIN,
                end=endpoint(),
                color=YELLOW,
                thickness=0.035,
                height=0.18,
                base_radius=0.08
            )
        )
        self.add(vector)
        self.wait(1)
        # Move from |0> to |+>
        # This follows the same state trajectory
        # as a Hadamard applied to |0>.
        self.play(
            theta.animate.set_value(PI / 2),
            run_time=3
        )
        self.wait(1)
        # Apply Rz(phi): rotate around equator
        self.play(
            phi.animate.set_value(TAU),
            run_time=6,
            rate_func=linear
        )
        self.wait(2)
