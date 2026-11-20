"""
 ####################################################################
  Ising2D.py

  2D Ising model

  Modified   By   Reason
  --------   --   ------
  20-Nov-26  CBL  Original

  References:
  
  Notes:
  ####################################################################
"""
# My imports
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.constants   as konst

class Ising2D:
    def __init__(self):
        """
        Initialize the model. 
        """
        self.N = 64       # lattice size
        self.J = 1.0      # Spin-Spin coupling strength
        self.T = 1.5      # Temperature in dimensionless units. 
        self.h = 0.0      # Magnetic field, or coupling energy in Joules = -uBs_i

        self.rng = np.random.default_rng(42)
        self.Reset()

    def Reset(self):
        # Random initial spins of: +1 or -1
        self.spins = self.rng.choice([-1,1], size=(self.N,self.N))

    def PlotInitial(self):
        plt.figure(figsize=(6,6))
        plt.imshow(self.spins, cmap="coolwarm", vmin=-1, interpolation="nearest")
        plt.title("Initial random configuration")
        plt.show()

    def energy_per_spin(self):
        neighbors = (
            np.roll(self.spins, -1, axis=0)
            + np.roll(self.spins, -1, axis=1)
        )
        E = -self.J * np.sum(self.spins*neighbors)
        E -= self.h * np.sum(self.spins)
        return E/self.spins.size

    def metropolis_sweep(self):
        """
        metropolis sweep
        Each sweep attempts N^2 spin flips. The four nearest neighbors determine the energy change. 
        """
        N, M = self.spins.shape
        for _ in range(N * M):
            i = self.rng.integers(N)
            j = self.rng.integers(M)

            # periodic boundry conditions
            neighbors = (
                self.spins[(i + 1) % N, j] 
                + self.spins[(i-1)%N, j]
                + self.spins[i, (j+1)%M]
                + self.spins[i, (j-1)%M]
            )
            dE = 2 * self.spins[i,j] * (self.J * neighbors + self.h)
            if dE < 0 or self.rng.random() < np.exp(-dE/self.T) :
                self.spins[i,j] *= -1

    def Magnetization(self):
        """
        @return the magnetization over the full lattice. 
        """
        magnetization = np.mean(self.spins)
        print(f"Magnetization: {magnetization: .4f}")
        return magnetization

    def Temperature(self):
        """
        @return the physical temperature in K
        J is not in joules, assume that the coupling is about 1meV
        """
        T_physical = self.J*1.0e-3 * konst.eV *self.T/konst.k
        print(f"Actual temperature: {T_physical:.2f} K")
        return T_physical
        
    def CurrentState(self):
        """
        Print out the Magnetization and current energy per spin a this time step. 
        """
        energy = self.energy_per_spin()
        print(f"Magnetization: {np.mean(self.spins):.4f}")
        print(f"Energy per spin: {energy:.4f}")

if __name__ == '__main__':
    i2d = Ising2D()
    i2d.PlotInitial()
    # Now evolve the system 
    # Observe after 0, 10 50 200 1000 iterations

    checkpoints = [0, 10, 50, 200, 1000]
    #checkpoints = [0, 100, 500, 2000, 10000]

    fig, axes = plt.subplots(1, len(checkpoints),figsize=(16,4))

    completed = 0

    for ax, target in zip(axes, checkpoints):
        for _ in range(target-completed):
            i2d.metropolis_sweep()
        completed = target

        ax.imshow( i2d.spins, cmap="coolwarm", vmin=-1, vmax=1, interpolation="nearest")
        ax.set_title(f"{target} sweeps")
        ax.axis("off")

        # per checkpoint
        i2d.CurrentState()
    plt.tight_layout()
    plt.show()
