from PySpice.Spice.Netlist import Circuit
import matplotlib.pyplot as plt

# Initialize the circuit.
circuit = Circuit('Sinusoidal Voltage Source Example')

# Add a Sinusoidal Voltage Source to the circuit,  
# and connect it between node input and GND.
circuit.SinusoidalVoltageSource(1, 'input', circuit.gnd, 
                                amplitude=2.0, 
                                frequency=1e3, 
                                offset=2.5)
# Add a 10kΩ resistor (R1), 
# and connect it between node input and output. 
circuit.R(1, 'input', 'output', 10e3)

# Initializes the circuit simulator with a specified operating 
# temperature of 25°C and a nominal temperature of 25°C.
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# Performs a transient simulation over the specified period.
analysis = simulator.transient(step_time=1e-6, end_time=10e-3)

# Get the voltages for node input.
Vin = analysis['input']

# Plotting the results.
plt.figure(figsize=(10, 6))
plt.plot(analysis.time * 1e3, Vin, '-g')
plt.title('Sinusoidal Voltage Source Example')
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [V]')
plt.xlim(0, 10)  # limit between 0 and 10ms.
plt.ylim(0, 5)  # limits between 0V and 5V.
plt.grid(True)
plt.tight_layout()
plt.show()