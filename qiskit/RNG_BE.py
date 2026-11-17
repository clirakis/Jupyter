# #####################################################################
# RNG_BE.py
#
# USING REAL BACKEND!
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
# 13-Nov-26 CBL Updated to include a loop to talk via OSC
# 17-Nov-26 CBL added in real backend
#
# References 
#    https://docs.quantum.ibm.com/guides/install-qiskit 
#    https://docs.quantum.ibm.com/guides/hello-world
#    https://qiskit-community.github.io/qiskit-dynamics/
#    https://pypi.org/project/qiskit/
#    https://docs.quantum.ibm.com/api/qiskit/visualization
#
# OSC/UDP interface
# https://docs.cycling74.com/legacy/max5/refpages/max-ref/udpreceive.html
# https://python-osc.readthedocs.io/en/latest/
# https://python-osc.readthedocs.io/en/latest/client.html#module-pythonosc.udp_client"
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

from qiskit.quantum_info import SparsePauliOp
from qiskit.quantum_info import Pauli
from scipy.spatial.transform import Rotation as R
# If you want to use the simulator this include is necessary
from qiskit_aer import AerSimulator
# for a real runtime environment use this.
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2

import struct

# OSC/UDP stuff
from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient

# system call
import time


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
"""
<Class to manage the OSC exchange<
I've got several things I'm setting up here. The method generic send,
just sends over the random number without any prefix other than /QRNG. 

You can kind of see how I'm building a larger vocabulary here.
There is a decision by the artist that needs to be made, where are you
going to do the heavy lifting, here or in the consumer (MAX/MSP or
Touch Designer or any  other OSC consumer.) My preference is here
since I'm very comfortable with Python and Jupyter. I will build in
an event loop that is just here AND I will also setup a way to
accept messages from the OSC consumer. 

Simple Vocabulary:

- /OSCnumber [Frequency, Phase] - send a frequency phase pair to the
             oscillator number.
- /QRNG value - just send a raw random number. 

There is a companion set of patches, programs or whatever is the name that
go with this. The MAX/MSP one is called UDP5 and has examples of how I
parse the messages. 
"""

class OSC_RxTx:
    """
    Very simple wrapper for OSC exchange. 
    Message content is very simple. Choosing to potentially have multiple oscillators and other controllers. 
    The OSC address string is therefore OBJECT INSTANCE
    """
    def __init__(self):
        """
        MAX/MSP or Touch Designer is the server. We are the client. It is kind of a coin toss as to which is
        which but I decided this makes the most sense to me. I've hard coded the address to localhost
        and the port to 9001. Change at your leisure. 
        """
        self.clientTx = SimpleUDPClient("127.0.0.1", 9001)
        self.clientRx = SimpleUDPClient("127.0.0.1", 9002)

    def GenericSend(self, val):
        """
        Just send a value over, let the receiving program do the heavy lifting. 
        """
        self.clientTx.send_message("/QRNG", val)

    def FreqPhase(self, f=440.0, phi=0.0, osc=1):
        """
        Send Frequency phase pair. 
        @param f - frequency
        @param phi - phase
        """
        to_send = "/osc/"+str(osc)
        self.clientTx.send_message(to_send,[f,phi])
        
    def Commands(self):
        """
        Check to see if there are any messages to us from the server. 
        The argument on get messages is the timeout for waiting for an 
        inbound message. The caller is responsible for checking that
        there is a message of value. 

        This is kinda tricky and will come back to this later. 
        """
        messages = self.clientRx.get_messages(2)
        
        #for msg in messages:
        #    print("Address: ", msg.address, " Data: ", msg.params)
        print(dir(messages))

    def __del(self):
        """
        Do any clean up when we are done. 
        """
        self.client.close()


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
class RNG:
    def __init__(self):
        """
        Initialize all the services we will need.
        @param use_simulator - set to true (default) if wanted.
        The following parameters are my credentials to run on real hardware
        """
        self.MyDebug       = False
        
        # 1. Authenticate and connect to IBM Quantum
        # (Run QiskitRuntimeService.save_account(channel="ibm_quantum", token="YOUR_API_TOKEN") once beforehand)
        # This call should load my token from local storage. 
        service = QiskitRuntimeService()

        # 2. Select the least busy real quantum computer with at least 2 qubits
        backend = service.least_busy(operational=True, simulator=False, min_num_qubits=2)
        print(f"Using backend: {backend.name}")

            
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
        self.qc   = QuantumCircuit(qreg, creg)
        #
        #
        # Create the quantum circuit 
        # This assumes that the resources have been previously allocated. 
        # The Hadamard gate puts the qubit into the state ${1\over {\sqrt{2}}}(\ket{0} + \ket{1})$
        #
        #
        # 
        # Create the OSC connection
        #
        self.pOSC = OSC_RxTx()

        # MOVE THIS TO A METHOD.
        #
        # SETUP THE CIRCUIT. 
        # Apply a hadamard on qubit 0 - this creates equal path case, superposition
        # The Hadamard gate can also be expressed as a 90º rotation
        # around the Y-axis, followed by a 180º around the X-axis. 
        #
        self.qc.h(0)
        # finally perform a measurement
        # qubit 0 results stored in classical register 0
        qc_measured = self.qc.measure(0, 0)
        # And make a pretty picture of the circuit.
        #
        # This may be commented out. 
        #qc.draw(output='mpl')
        #plt.show()
        # Create an estimator - this gives the expectation value of each system.
        # the number of shots is the number of times that the experiment is
        # replicated to produce statistics. 
        # In the estimator, you specify the precision instead, this is the
        # default and can be overriden in 
        # the estimator run command. Default precision is 0
        #
        # reference: https://quantum.cloud.ibm.com/docs/en/api/qiskit-ibm-runtime/sampler-v2
        #
        # 4. Transpile the circuit to match the hardware's physical
        # qubit layout and native gates
        pm = generate_preset_pass_manager(
            backend=backend, optimization_level=1)
        self.isa_circuit = pm.run(self.qc)
        self.sampler = SamplerV2(mode=backend)
                  

    # RNG - get a group of numbers as needed. 
    def GetRNG(self):
        """
        Tell the sampler how you want to do the program. 
        qc is the quantum circuit
        The following reference has a very good example on how to use this. 
        https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.primitives.StatevectorSampler
        scroll down to the example where the 'pub' is created. 

        pub stands for Primitive unified bloc
        multiple pubs may be submitted. 
        details on pubs - https://quantum.cloud.ibm.com/docs/en/guides/primitive-input-output

        details on options - https://quantum.cloud.ibm.com/docs/en/guides/specify-runtime-options

        estimator pubs
        quantum circuit
        A list of one or more observables: [ObservableArrayLike, Pauli, SparsePauliOp, PauliList, str]
        Collection of parameter objects, in this case theta
        
        Need to introduce the number of shots in this system. 

        lets say I want to use this single qubit to generate a series of
        16 bit numbers. Then I want the number of shots to 
        be evenly divisable by 16
        """
        # Declare we want 16 bit numbers, we can always change
        # this or make it tranparent.
        if self.MyDebug:
            print("GetRNG")
            
        BitLength = 16
        DesiredNumbers = 100
        NShots = DesiredNumbers * BitLength
        # Run the job
        job = self.sampler.run([self.isa_circuit],shots=NShots)
        
        # get the results
        result = job.result()[0] # only 1 qubit
        #
        # get the individual shot data
        shot_data = result.data['cbit'].array
        #
        # gyrations to get the data into the format we like. numpy call
        div = np.split(shot_data, DesiredNumbers)
        L = len(div)
        xy = np.zeros(L)
        for i in range(L):
            xy[i] = bit2N(div[i])
        return xy


    def Loop(self, N):
        """
        test out sending to external program here. Loop over 16 bit numbers
        Lets make the upper limit 8KHz (2^13) rather than 65535 (2^16)

        User changes go here. 
        """

        scale = 8192/65536  # how do you want to use these 16 bit numbers? 
        #
        # Set the outer loop for how many times you want to do this. It is
        # poor use of resources to go back to the quantum computer for
        # every single random number, it is better to 
        # get a batch at a time. 
        #
        # the value in the call range sets the number of iterations on
        # the outer loop. 
        for i in range(N):
            # Get a batch of random numbers from the QC.
            xy = self.GetRNG()
            for val in xy:
                #freq = scale * val
                freq = val%8192
                # send the frequency to oscillator 1 - USER to change here. 
                self.pOSC.FreqPhase(freq,0.0, 1)
                # Change sleep time as needed. - LONG TERM get a two way conversation between the two processes to make requests
                time.sleep(0.5)
        # this is me just setting it to a plesant tone at the end. 
        self.pOSC.FreqPhase(110.0, 0.0, 1)

    def SetDebug(self, value=True):
        self.MyDebug = value
                  
def PlotMe(xy):
    plt.hist(xy)
    plt.grid()
    print('This should be realitively uniform., close figure to continue.')
    plt.show()
    
if __name__ == '__main__':
 
    rng = RNG()
    rn = rng.GetRNG()
    # debug, uncomment to see distribution of RN.
    PlotMe(rn)
    #rng.Loop(2)
