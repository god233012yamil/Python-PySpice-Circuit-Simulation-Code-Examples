from PySpice.Spice.Netlist import Circuit
import matplotlib.pyplot as plt

# Initialize the circuit.
circuit = Circuit('Pulse Voltage Source Example')

# Add a Pulse Voltage Source to the circuit,  
# and connect it between node input and GND.
circuit.PulseVoltageSource(1, 'input', circuit.gnd, 
                           initial_value=0.5, # 0.5V
                           pulsed_value=4.5,  # 4.5V
                           pulse_width=1e-3,  # 1ms
                           period=2e-3,       # 2ms
                           rise_time=0.1e-6,  # 0.1us
                           fall_time=0.1e-6)  # 0.1us       

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
plt.title('Pulse Voltage Source Example')
plt.xlabel('Time [ms]')
plt.ylabel('Voltage [V]')
plt.xlim(0, 10)  # limit between 0 and 10ms.
plt.ylim(0, 5)  # limits between 0V and 5V.
plt.grid(True)
plt.tight_layout()
plt.show()