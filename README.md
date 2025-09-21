# QuantumBox

An interactive quantum mechanics visualization toolkit built with Python and Google's Cirq framework.  
QuantumBox provides simulations of infinite and finite square wells with side-by-side visualization and basic quantum circuit analogues.

## Features

- Interactive parameter control for well dimensions and particle properties  
- Real-time visualization of wavefunctions and probability densities  
- Quantum circuit simulation using Cirq  
- Time evolution animations of superposition states  
- Comparison tools for infinite vs finite square wells  

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/n0sync/QuantumBox.git
cd QuantumBox
```

## Usage

Create a virtual environment (recommended) and run:

```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Project Structure

```bash
QuantumBox/
├── main.py                     # Entry point
├── src/                        
│   ├── infinite_square.py      # Infinite square well implementation
│   └── finite_square.py        # Finite square well implementation
└── visualization/            
    └── visualizer.py           # Visualization utilities
```

## Contributing

Contributions are welcome.

Potential extensions include:
- Harmonic oscillators
- Double wells
- 2D and 3D quantum systems
- More advanced quantum circuit mappings

## License

This project is licensed under the MIT License – see the LICENSE file for details.