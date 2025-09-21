import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.infinite_sqaure import InfiniteSquareWell
from src.finite_square import FiniteSquareWell

def user_input():
    print("QuantumBox Interactive Parameters")
    print("=" * 35)
    
    length = float(input("Infinite well length [1.0]: ") or "1.0")
    mass = float(input("Particle mass [1.0]: ") or "1.0")
    hbar = float(input("Reduced Planck constant [1.0]: ") or "1.0")
    
    width = float(input("Finite well width [2.0]: ") or "2.0")
    depth = float(input("Finite well depth [50.0]: ") or "50.0")
    
    num_points = int(input("Grid resolution [1000]: ") or "1000")
    max_n = int(input("Max quantum number to show [5]: ") or "5")
    
    return {
        'infinite': {'length': length, 'mass': mass, 'hbar': hbar, 'num_points': num_points},
        'finite': {'width': width, 'depth': depth, 'mass': mass, 'hbar': hbar, 'num_points': num_points},
        'max_n': max_n
    }

def infinite_well(params):
    well = InfiniteSquareWell(**params['infinite'])
    max_n = params['max_n']
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Infinite Square Well (L={params["infinite"]["length"]})', fontsize=16)
    
    energies = [well.energy_level(n) for n in range(1, max_n + 1)]
    ax1.barh(range(1, max_n + 1), energies, color='cyan', alpha=0.7)
    ax1.set_xlabel('Energy')
    ax1.set_ylabel('Quantum Number n')
    ax1.set_title('Energy Levels')
    
    colors = plt.cm.viridis(np.linspace(0, 1, max_n))
    for n, color in zip(range(1, max_n + 1), colors):
        psi = well.wavefunction(n)
        ax2.plot(well.x, psi, color=color, label=f'n={n}', linewidth=2)
    ax2.set_xlabel('Position x')
    ax2.set_ylabel('ψ(x)')
    ax2.set_title('Wavefunctions')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    for n, color in zip(range(1, max_n + 1), colors):
        prob = well.probability_density(n)
        ax3.plot(well.x, prob, color=color, label=f'n={n}', linewidth=2)
    ax3.set_xlabel('Position x')
    ax3.set_ylabel('|ψ(x)|²')
    ax3.set_title('Probability Densities')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    quantum_dist = well.simulate_quantum_measurement(n_qubits=4, shots=2000)
    positions = np.linspace(0, params['infinite']['length'], len(quantum_dist))
    ax4.bar(positions, quantum_dist, width=positions[1]-positions[0], color='magenta', alpha=0.7)
    ax4.set_xlabel('Position')
    ax4.set_ylabel('Probability')
    ax4.set_title('Quantum Circuit Simulation')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def finite_well(params):
    well = FiniteSquareWell(**params['finite'])
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Finite Square Well (w={params["finite"]["width"]}, V0={params["finite"]["depth"]})', fontsize=16)
    
    potential = well.potential(well.x)
    ax1.plot(well.x, potential, 'white', linewidth=3, label='Potential V(x)')
    ax1.set_ylim(-5, well.V0 + 5)
    ax1.set_xlabel('Position x')
    ax1.set_ylabel('Potential V(x)')
    ax1.set_title('Finite Square Well Potential')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    bound_states = well.bound_wavefunction()
    colors = plt.cm.plasma(np.linspace(0, 1, len(bound_states)))
    
    for i, (energy, psi) in enumerate(bound_states):
        color = colors[i]
        ax2.plot(well.x, psi, color=color, linewidth=2, label=f'E={energy:.2f}')
        ax1.axhline(y=energy, color=color, linestyle='--', alpha=0.7)
        
    ax2.set_xlabel('Position x')
    ax2.set_ylabel('ψ(x)')
    ax2.set_title('Bound State Wavefunctions')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    for i, (energy, psi) in enumerate(bound_states):
        color = colors[i]
        prob = np.abs(psi)**2
        ax3.plot(well.x, prob, color=color, linewidth=2, label=f'E={energy:.2f}')
        
    ax3.set_xlabel('Position x')
    ax3.set_ylabel('|ψ(x)|²')
    ax3.set_title('Probability Densities')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    tunnel_dist = well.quantum_tunneling(n_qubits=5, shots=2000)
    positions = np.linspace(-3*well.a, 3*well.a, len(tunnel_dist))
    ax4.bar(positions, tunnel_dist, width=positions[1]-positions[0], color='cyan', alpha=0.7)
    ax4.axvline(x=-well.a, color='red', linestyle='--', alpha=0.7, label='Well boundary')
    ax4.axvline(x=well.a, color='red', linestyle='--', alpha=0.7)
    ax4.set_xlabel('Position')
    ax4.set_ylabel('Probability')
    ax4.set_title('Quantum Tunneling Simulation')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def animate_superposition(params):
    well = InfiniteSquareWell(**params['infinite'])
    
    n1 = int(input("First quantum number for superposition [1]: ") or "1")
    n2 = int(input("Second quantum number for superposition [2]: ") or "2")
    c1 = float(input("Amplitude for first state [0.707]: ") or "0.707")
    c2 = float(input("Amplitude for second state [0.707]: ") or "0.707")
    
    norm = np.sqrt(c1**2 + c2**2)
    coeffs = [c1/norm, c2/norm]
    quantum_nums = [n1, n2]
    times = np.linspace(0, 2, 100)
    
    prob_evolution = well.time_evolve(coeffs, quantum_nums, times)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, params['infinite']['length'])
    ax.set_ylim(0, np.max(prob_evolution) * 1.1)
    ax.set_xlabel('Position x')
    ax.set_ylabel('|ψ(x,t)|²')
    ax.set_title(f'Superposition of n={n1} and n={n2}')
    ax.grid(True, alpha=0.3)
    
    line, = ax.plot([], [], 'cyan', linewidth=3)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    
    def animate(frame):
        line.set_data(well.x, prob_evolution[frame])
        time_text.set_text(f'Time = {times[frame]:.2f}')
        return line, time_text
    
    anim = animation.FuncAnimation(fig, animate, frames=len(times), 
                                 interval=100, blit=True, repeat=True)
    plt.show()
    return anim

def compare_wells(params):
    infinite_well = InfiniteSquareWell(**params['infinite'])
    finite_well = FiniteSquareWell(**params['finite'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Infinite vs Finite Square Wells', fontsize=16)
    
    colors = plt.cm.viridis(np.linspace(0, 1, 3))
    for n, color in zip(range(1, 4), colors):
        psi_inf = infinite_well.wavefunction(n)
        ax1.plot(infinite_well.x, psi_inf, color=color, linewidth=2, label=f'n={n}')
    
    ax1.set_xlabel('Position x')
    ax1.set_ylabel('ψ(x)')
    ax1.set_title('Infinite Well Wavefunctions')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    bound_states = finite_well.bound_wavefunction()
    x_finite = finite_well.x
    
    potential = finite_well.potential(x_finite)
    ax2_twin = ax2.twinx()
    ax2_twin.plot(x_finite, potential/10, 'white', linewidth=2, alpha=0.5, label='V(x)/10')
    ax2_twin.set_ylabel('Potential/10')
    
    colors = plt.cm.plasma(np.linspace(0, 1, min(3, len(bound_states))))
    for i, (energy, psi) in enumerate(bound_states[:3]):
        ax2.plot(x_finite, psi, color=colors[i], linewidth=2, label=f'E={energy:.1f}')
    
    ax2.set_xlabel('Position x')
    ax2.set_ylabel('ψ(x)')
    ax2.set_title('Finite Well Wavefunctions')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
