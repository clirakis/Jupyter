import numpy as np

# create your time array, a little easier than how you were doing it. 
time_array = np.arange(0.0,4.0,0.25)
#
#
spec_data = []

print('initial')
for i in range(10):
    voltage = np.random.rand()
    spec_data = np.append(spec_data,voltage)
    print(' new data.', spec_data)
