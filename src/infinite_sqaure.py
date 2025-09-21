import numpy as np
import cirq


class InfiniteSquareWell:
    def __init__(self, length=1.0, mass=1.0, hbar=1.0, num_points=100):
        self.L = length
        self.m = mass
        self.hbar = hbar
        self.N = num_points
        self.x = np.linspace(0, length, num_points)
        self.dx = length / (num_points - 1)
        
    def energy_level(self, n):
        return (n * np.pi * self.hbar)**2 / (2 * self.m * self.L**2)
    
    def wavefunction(self, n, x=None):
        if x is None:
            x = self.x
        return np.sqrt(2/self.L) * np.sin(n * np.pi * x / self.L)
    
    def probability_density(self, n, x=None):
        psi = self.wavefunction(n, x)
        return np.abs(psi)**2
    
    def superposition_state(self, coefficients, quantum_numbers, t=0):
        psi = np.zeros(len(self.x), dtype=complex)
        for c, n in zip(coefficients, quantum_numbers):
            E_n = self.energy_level(n)
            phase = np.exp(-1j * E_n * t / self.hbar)
            psi += c * self.wavefunction(n) * phase
        return psi
    
    def time_evolve(self, coefficients, quantum_numbers, times):
        results = []
        for t in times:
            psi = self.superposition_state(coefficients, quantum_numbers, t)
            prob = np.abs(psi)**2
            results.append(prob)
        return np.array(results)
    
    def quantum_circuit(self, n_qubits=4):
        qubits = cirq.LineQubit.range(n_qubits)
        circuit = cirq.Circuit()
        
        for i, qubit in enumerate(qubits):
            if i % 2 == 0:
                circuit.append(cirq.H(qubit))
        
        for i in range(len(qubits)-1):
            circuit.append(cirq.CNOT(qubits[i], qubits[i+1]))
            
        return circuit, qubits
    
    def simulate_quantum_measurement(self, n_qubits=4, shots=1000):
        circuit, qubits = self.quantum_circuit(n_qubits)
        circuit.append(cirq.measure(*qubits, key='result'))
        
        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=shots)
        measurements = result.measurements['result']
        
        position_counts = np.zeros(2**n_qubits)
        for measurement in measurements:
            index = sum(bit * (2**i) for i, bit in enumerate(measurement))
            position_counts[index] += 1
            
        return position_counts / shots