from PySpice.Spice.Netlist import Circuit
import matplotlib.pyplot as plt

# Initialize the circuit.
circuit = Circuit('PWL Voltage Source Example')

# Add a Piecewise Linear Voltage Source to the circuit,  
# and connect it between node input and GND.
circuit.PieceWiseLinearVoltageSource(1, 'input', circuit.gnd, 
                                     values=[(0, 0),     # 0, 0V
                                             (1e-3, 1),  # 1ms, 1V
                                             (2e-3, 4),  # 2ms, 4V
                                             (3e-3, 2)]) # 3ms, 2V

# Add a 10kΩ resistor (R1), 
# and connect it between node input and output. 
circuit.R(1, 'input', 'output', 10e3)

# Initializes the circuit simulator with a specified operating 
# temperature of 25°C and a nominal temperature of 25°C.
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# Performs a transient simulation over the specified period.
analysis = simulator.transient(step_time=1e-6, end_time=10e-3)

# Get the voltages for output node.
Vin = analysis['output']

# Plotting the results.
plt.figure(figsize=(10, 6))
plt.plot(analysis.time * 1e3, Vin, '-g')
plt.title('PWL Voltage Source Example')
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [V]')
plt.xlim(0, 10)  # limit between 0 and 10ms.
plt.ylim(0, 5)  # limits between 0V and 5V.
plt.grid(True)
plt.tight_layout()
plt.show()