from PySpice.Spice.Netlist import Circuit
import matplotlib.pyplot as plt

# Initialize the circuit.
circuit = Circuit('DC Voltage Source Example')

# Add a DC voltage source to the circuit,  
# and connect it between nodes input and GND.
circuit.V(1, 'input', circuit.gnd, 'DC 5V')
# Add a 10kΩ resistor (R1) to the circuit,  
# and connect it between nodes input and output. 
circuit.R(1, 'input', 'output', 10e3)

# Initializes the circuit simulator with a specified operating 
# temperature of 25°C and a nominal temperature of 25°C.
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# Performs a transient simulation over the specified period.
analysis = simulator.transient(step_time=1e-3, end_time=100e-3)

# Get the voltages for node input.
Vin = analysis['input']

# Plotting the results.
plt.figure(figsize=(10, 6))
plt.plot(analysis.time * 1e3, Vin, '-g')
plt.title('DC Voltage Source Example')
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [V]')
plt.xlim(0, 100)  # limit between 0 and 100ms.
plt.ylim(4.0, 5.5)  # limits between 4.0V and 5.5V.
plt.grid(True)
plt.tight_layout()
plt.show()