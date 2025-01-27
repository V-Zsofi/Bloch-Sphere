# Bloch-Sphere

This project implements a Bloch Sphere Simulator, a tool for visualizing quantum bit (qubit) states and simulating the application of quantum gates. The Bloch sphere representation is a crucial concept in quantum computing, as it provides a geometric visualization of the state of a qubit.

## Features

### 3D Bloch Sphere Visualization
The Bloch Sphere is updated in real-time, allowing users to observe the quantum bit states. Users can rotate the sphere to view the states from different angles.

### Alpha and Beta Angles
Two sliders allow users to adjust the alpha and beta angles of the quantum bit, which influences its state on the Bloch Sphere.

### Formula Input
Users can define quantum states by adjusting the alpha and beta parameters, with the Bloch Sphere updating in real time based on these values.

### Quantum Gates
Supports the following quantum gates:
- Pauli-X, Pauli-Y, Pauli-Z
- Hadamard Gate (H gate)
- Custom gate defined by a user-provided matrix.

### Stack History
The simulator logs all operations performed on the quantum bit, allowing users to undo the last 5 actions for better control.

### Default States
Users can quickly switch between standard quantum states such as ∣0⟩, ∣1⟩, ∣+⟩, and ∣-⟩ using dedicated buttons.

### Undo and Init Buttons
- If a user mistakenly applies an operation, the **Undo** button allows them to revert the last change, making it easier to experiment and correct mistakes.  
- The **Init** button resets the Bloch Sphere to its initial state, offering users a fresh start for their quantum experiments and visualizations.

## Installation

To run the Bloch Sphere Visualization program, you'll need the Python interpreter and the `src` folder. Follow these steps to ensure all necessary libraries are installed and the program runs correctly:

1. Open the Command Prompt (CMD) and navigate to the `Bloch-Sphere` folder.
2. To install the required packages and launch the program, run the following command:
   
   ```bash
   pip install -r requirements.txt && python src/main.py
   ```
This command will automatically install all the libraries listed in the requirements.txt file and start the visualization program.