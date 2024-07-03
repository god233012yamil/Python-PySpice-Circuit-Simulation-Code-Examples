import numpy as np
import matplotlib.pyplot as plt
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *
from PySpice.Probe.Plot import plot
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

# This is the initial voltage of the pulse source before it starts pulsing 
initial_voltage = 0    # 0V
# This is the voltage level to which the source will pulse. 
pulsed_voltage = 5     #5V
# The duration for which the pulsed voltage is maintained before it returns 
# to the initial voltage.
pulse_width = 5e-3     # 1ms
# This is the total period of the pulse cycle, including the pulse width and 
# the time until the next pulse begins.
period = 10e-3         # 10ms
# This is the delay before the pulse starts.
delay_time = 1e-3
# This parameter defines the time it takes for the voltage to rise from the 
# initial to the pulsed voltage.
rise_time = 0.1e-3 
# This is the time it takes for the voltage to fall from the pulsed voltage 
# back to the initial voltage.
fall_time = 0.1e-3 

# Initialize the circuit.
circuit = Circuit('Enhanced MOSFET Parameterized Model Test Circuit')

# Define the NMOS transistor with detailed parameters.
circuit.model('IPD088N06N3', 'NMOS', RG=0.9, VTO=4.35, RD=3.88e-3, RS=1.29e-3, 
              RB=2.76e-3, KP=94.9, LAMBDA=0.01, CGDMIN=7e-12, CGDMAX=0.75e-9, 
              A=2.5, CJO=2.16e-9, M=0.3, IS=5.8e-12, VJ=0.9, N=1.06, TT=30e-9, 
              KSUBTHRES=0.1, MFG='Infineon', RON=8.8e-3, QG=36e-9)

# Define the NMOS transistor instance
# Syntax: M<name> <drain> <gate> <source> <bulk> <model>
# Here, 'source' is used for both the source and bulk terminals
circuit.MOSFET(1, 'drain', 'gate', 'source', 'source', model='IPD088N06N3')

# Define the Drain voltage supply (Vdd=10V).
Vdrain = circuit.V(1, 'Vdd', circuit.gnd, 10)  

# Define a pulse voltage source. It will be used as the gate voltage.
Vgate = circuit.PulseVoltageSource('Pulse', 
                           'Vg', circuit.gnd, 
                           initial_voltage, 
                           pulsed_voltage,                             
                           pulse_width, 
                           period,
                           delay_time=delay_time,
                           rise_time=rise_time,
                           fall_time=fall_time,
                           phase=None, 
                           dc_offset=0)  

# Define a resistor in the drain path
circuit.R(1, 'Vdd', 'drain', 1e3)  # Drain resistor (1kΩ)

# Define a resistor in the gate path
circuit.R(2, 'Vg', 'gate', 10)  # Drain resistor (10Ω)

# Define a resistor in the source path
circuit.R(3, 'source', circuit.gnd, 10)  # Source resistor (10Ω)

# Simulate the circuit
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1e-6, end_time=30e-3)

# Create a new figure object and set the size of the figure.
plt.figure(figsize=(12, 8))

# Plot the gate voltage.
ax1 = plt.subplot(3, 1, 1)
# plt.plot(analysis.time * 1e3, analysis['gate'], label='Gate Voltage')
plt.plot(np.array(analysis.time * 1e3), np.array(analysis["gate"]), '-r', 
         label='Gate Voltage')
plt.title('Gate Voltage')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.xlim(0, 30)  # limit between 0 and 30ms.
plt.ylim(0, 10)  # limits between 0 and 10V.
ax1.xaxis.set_major_locator(MultipleLocator(3))  # Major ticks every 3 ms
ax1.xaxis.set_minor_locator(AutoMinorLocator(6))  # 6 minor ticks per major tick
plt.grid(True, which='both')  # Show grid for both major and minor ticks

# Plot the Drain voltage.
ax2 = plt.subplot(3, 1, 2)
# plt.plot(analysis.time * 1e3, analysis['drain'], label='Drain Voltage')
plt.plot(np.array(analysis.time * 1e3), np.array(analysis['drain']), '-b', 
         label="Drain Voltage")
plt.title('Drain voltage')
plt.xlabel('Time (ms)')
plt.ylabel('Voltage (V)')
plt.xlim(0, 30)  # limit between 0 and 30ms.
plt.ylim(0, 12)  # limits between 0 and 12V.
ax2.xaxis.set_major_locator(MultipleLocator(3))  # Major ticks every 3 ms
ax2.xaxis.set_minor_locator(AutoMinorLocator(6))  # 6 minor ticks per major tick
plt.grid(True, which='both')  # Show grid for both major and minor ticks

# Plot the Drain current.
ax3 = plt.subplot(3, 1, 3)
plt.plot(np.array(analysis.time * 1e3), 
         ((np.array(analysis['Vdd']) - np.array(analysis['drain'])) / circuit['R1'].resistance) * 1000, 
         '-g', label="Drain Current")
plt.title('Drain Current')
plt.xlabel('Time (ms)')
plt.ylabel('Current (mA)')
plt.xlim(0, 30)  # limit between 0 and 30ms.
plt.ylim(0, 20)  # limit between 0 and 20mA.
ax3.xaxis.set_major_locator(MultipleLocator(3))  # Major ticks every 3 ms
ax3.xaxis.set_minor_locator(AutoMinorLocator(6))  # 6 minor ticks per major tick
plt.grid(True, which='both')  # Show grid for both major and minor ticks

plt.tight_layout()
plt.show()

