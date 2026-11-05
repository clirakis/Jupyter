# #####################################################################
# RNG.py
#
# Use a single qubit (or multiples) to create a series of random numbers.
# Going to try out a number of ideas. <br> 
#
#    - just sample a series of qubits without initialization
#    - initalize to ground state and allow $T_2$ (shorter than $T_1$)
#      to evolve, ie do a Hadamard then a X or Y rotation
#
# Modification history
# Modified By  Reason
# 20-Aug-25 CBL Original in jupyter notebook form.
# 05-Nov-26 CBL Moved to python script for those who don't want to use Jupyter
#
# References 
#    https://docs.quantum.ibm.com/guides/install-qiskit 
#    https://docs.quantum.ibm.com/guides/hello-world
#    https://qiskit-community.github.io/qiskit-dynamics/
#    https://pypi.org/project/qiskit/
#    https://docs.quantum.ibm.com/api/qiskit/visualization
#
# Notes 
#
# If you want to run this on a real processor, you need to apply for an
# account and get a token.
#
# This example uses the AER simulator package. I am using the sampler rather
# than the estimator in this case. The estimator returns individual
# expection values. The sampler will return the value of each shot. 
#
#
# to install qiskit please create a virtual python enviroment
# in your home directory using the command
# python -m venv .envQiskit
#
# enable this enviroment by issuing the command
# . .envQiskit/bin/activate
#
# #####################################################################
# my standard includes
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy.constants as const
# Qiskit imports
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Parameter
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
from qiskit.quantum_info import SparsePauliOp
from qiskit.quantum_info import Pauli
from scipy.spatial.transform import Rotation as R

import struct
#
# END OF IMPORTS
#
#
# ======================= HELPER FUNCTIONS ====================
#
def bit2N(s):
    """
    helper function, create a number of arbitrary length depending on
    input list. 
    @param s - input string, need 8 input bits to produce one byte
    """
    rv = 0
    for i in range(len(s)):
        rv = rv + s[i] * np.power(2,i)
    return rv[0]

def SaveNumbers(x):
    """
    Save the sequence of numbers to a file.
    will modify this later to use UDP/OSC protocol to send
    to MAX/MSP later.
    """
    fd = open('numbers.txt','w')
    for n in x:
        fd.write(str(n))
    fd.close()
#
# ======================= END HELPER FUNCTIONS ====================
#
#
# Basic Concepts 
# Placing a qubit into a superposition state and then measuring it,
# should be a real random distribution 50% distribition of 1 and 0.
# We can either make a number of measurements on a single qubit and
# then make a binary string of arbitrary length OR select a number
# of qubits that are independent and do the same operation on all
# of them to make a string. The length of the single string or width
# of the circuit will determine the integer number size. If
# we call L the string length then the number sequence will be {0:$2^L$}. 
# Code description: 
#
#    - nqbit - number of qubits needed to run the experiment. 
#    - ncbit - number of classical bits needed - this is a register to
#              put the results in. 
#    - creg - a classical register to collect the results. 
#    - qreg - the register of quantum bits that will be run on a simulator
#             or back end. 
#    - nshots - number of measurements to be made per point or number
#               of times to perform the experiment. 
#    - qc     - The quantum circuit. 
#
# SETUP
# The code below sets up the overall system to run. It should be
# pretty well inline documented below.
#
# Instantiate the AER simulator
# with an account, you can specify a backend error model based off of
# one of the IBM systems if desired.
# 
sim = AerSimulator()
# Define the number of quantum bits. 
nqbit     = 1
# for using the sampler, we need some clasical bits to store the output data
ncbit     = 1
# Create the actual registers. 
creg = ClassicalRegister(ncbit, 'cbit')
qreg = QuantumRegister(nqbit)
# Create a very simple quantum circuit.
# https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.QuantumCircuit
# Here we tell the circuit that we want to use the quantum and
# classical registers we created above. 
qc   = QuantumCircuit(qreg, creg)
# Create an estimator - this gives the expectation value of each system. 
# the number of shots is the number of times that the experiment is
# replicated to produce statistics. 
# In the estimator, you specify the precision instead, this is the
# default and can be overriden in 
# the estimator run command. Default precision is 0
#
# reference: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/sampler-v2
#
sampler = SamplerV2()
#
#
# Create the quantum circuit 
# This assumes that the resources have been previously allocated. 
# The Hadamard gate puts the qubit into the state ${1\over {\sqrt{2}}}(\ket{0} + \ket{1})$
#
#
# Apply a hadamard on qubit 0 - this creates equal path case, superposition
# The Hadamard gate can also be expressed as a 90º rotation around the Y-axis, followed by a 180º around the X-axis. 
#
qc.h(0)
# finally perform a measurement
# qubit 0 results stored in classical register 0
qc_measured = qc.measure(0, 0)
# And make a pretty picture of the circuit.
qc.draw(output='mpl')
print("Close figure to continue running the program.")
plt.show()
#
#
# Tell the sampler how you want to do the program. 
# qc is the quantum circuit
# The following reference has a very good example on how to use this. 
# https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorSampler
# scroll down to the example where the 'pub' is created. 
#
# pub stands for Primitive unified bloc
# multiple pubs may be submitted. 
# details on pubs - https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output
#
# details on options - https://quantum.cloud.ibm.com/docs/en/guides/specify-runtime-options
#
# estimator pubs
# quantum circuit
# A list of one or more observables: [ObservableArrayLike, Pauli, SparsePauliOp, PauliList, str]
# Collection of parameter objects, in this case theta
# 
# Need to introduce the number of shots in this system. 
#
# lets say I want to use this single qubit to generate a series of
# 16 bit numbers. Then I want the number of shots to 
# be evenly divisable by 16
BitLength = 16
DesiredNumbers = 100
NShots = DesiredNumbers * BitLength
# Run the job
job = sampler.run([qc],shots=NShots)
# get the results
result = job.result()[0] # only 1 qubit
#
# show the count distribution
print('Results: ', result.data['cbit'].get_counts())
# get the individual shot data
shot_data = result.data['cbit'].array
print('Shot data: ', shot_data)
#
# gyrations to get the data into the format we like. 
div = np.split(shot_data, DesiredNumbers)
x = div[1]
print('Check conversion of a single set of bits into a byte: ', bit2N(x))
#
# Plot a histogram of the numbers
#
L = len(div)
xy = np.zeros(L)
for i in range(L):
    xy[i] = bit2N(div[i])
plt.hist(xy)
plt.grid()
print('This should be realitively uniform., close figure to continue.')
plt.show()

#
#
#
input ("Hit Enter to end this program:")
