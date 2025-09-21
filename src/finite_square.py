import numpy as np
from scipy.optimize import fsolve
import cirq


class FiniteSquareWell:
    def __init__(self, width=2.0, depth=10.0, mass=1.0, hbar=1.0, num_points=200):
        self.a = width / 2
        self.V0 = depth
        self.m = mass
        self.hbar = hbar
        self.N = num_points
        self.x = np.linspace(-3*self.a, 3*self.a, num_points)
        self.dx = self.x[1] - self.x[0]
        
    def potential(self, x):
        return np.where(np.abs(x) <= self.a, 0, self.V0)
    
    def bound_states(self):
        k0 = np.sqrt(2 * self.m * self.V0) / self.hbar
        bound_energies = []
        
        for n in range(1, 10):
            try:
                def even_equation(E):
                    if E >= self.V0 or E <= 0:
                        return float('inf')
                    k = np.sqrt(2 * self.m * E) / self.hbar
                    gamma = np.sqrt(2 * self.m * (self.V0 - E)) / self.hbar
                    return k * np.tan(k * self.a) - gamma
                
                E_guess = self.V0 * (n - 0.5) / 10
                E_solution = fsolve(even_equation, E_guess)[0]
                if 0 < E_solution < self.V0 and abs(even_equation(E_solution)) < 1e-6:
                    bound_energies.append(E_solution)
            except:
                pass
                
        for n in range(1, 10):
            try:
                def odd_equation(E):
                    if E >= self.V0 or E <= 0:
                        return float('inf')
                    k = np.sqrt(2 * self.m * E) / self.hbar
                    gamma = np.sqrt(2 * self.m * (self.V0 - E)) / self.hbar
                    return -k / np.tan(k * self.a) - gamma
                
                E_guess = self.V0 * n / 10
                E_solution = fsolve(odd_equation, E_guess)[0]
                if 0 < E_solution < self.V0 and abs(odd_equation(E_solution)) < 1e-6:
                    bound_energies.append(E_solution)
            except:
                pass
        
        return sorted(list(set(bound_energies)))
    
    def wavefunction(self, E, parity='even'):
        k = np.sqrt(2 * self.m * E) / self.hbar
        gamma = np.sqrt(2 * self.m * (self.V0 - E)) / self.hbar
        
        psi = np.zeros(len(self.x))
        
        inside = np.abs(self.x) <= self.a
        if parity == 'even':
            psi[inside] = np.cos(k * self.x[inside])
            A = np.cos(k * self.a)
            B = A * np.exp(gamma * self.a)
        else:
            psi[inside] = np.sin(k * self.x[inside])
            A = np.sin(k * self.a)
            B = A * np.exp(gamma * self.a)
        
        right = self.x > self.a
        left = self.x < -self.a
        
        if parity == 'even':
            psi[right] = B * np.exp(-gamma * self.x[right])
            psi[left] = B * np.exp(gamma * self.x[left])
        else:
            psi[right] = B * np.exp(-gamma * self.x[right])
            psi[left] = -B * np.exp(gamma * self.x[left])
        
        norm = np.trapz(psi**2, self.x)
        if norm > 0:
            psi /= np.sqrt(norm)
            
        return psi
    
    def bound_wavefunction(self):
        energies = self.bound_states()
        wavefunctions = []
        
        for i, E in enumerate(energies):
            parity = 'even' if i % 2 == 0 else 'odd'
            psi = self.wavefunction(E, parity)
            wavefunctions.append((E, psi))
            
        return wavefunctions
    
    def tunneling_probability(self, E, barrier_start, barrier_width):
        if E >= self.V0:
            return 1.0
        
        gamma = np.sqrt(2 * self.m * (self.V0 - E)) / self.hbar
        return np.exp(-2 * gamma * barrier_width)
    
    def quantum_circuit(self, n_qubits=5):
        qubits = cirq.LineQubit.range(n_qubits)
        circuit = cirq.Circuit()
        
        for qubit in qubits:
            circuit.append(cirq.H(qubit))
        
        for i in range(len(qubits)-1):
            circuit.append(cirq.CNOT(qubits[i], qubits[i+1]))
            circuit.append(cirq.rz(0.1)(qubits[i+1]))
        
        for i, qubit in enumerate(qubits):
            angle = 0.2 * (i - len(qubits)//2)
            circuit.append(cirq.ry(angle)(qubit))
            
        return circuit, qubits
    
    def quantum_tunneling(self, n_qubits=5, shots=1000):
        circuit, qubits = self.quantum_circuit(n_qubits)
        circuit.append(cirq.measure(*qubits, key='position'))
        
        simulator = cirq.Simulator()
        result = simulator.run(circuit, repetitions=shots)
        measurements = result.measurements['position']
        
        position_dist = np.zeros(2**n_qubits)
        for measurement in measurements:
            index = sum(bit * (2**i) for i, bit in enumerate(measurement))
            position_dist[index] += 1
            
        return position_dist / shots