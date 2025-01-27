import numpy as np
from numpy import dot, sqrt, array

# Pauli-X kapu osztály
class PauliXGate:
    @staticmethod
    def apply(state_vector):
        # Pauli-X mátrix definiálása
        pauli_x = np.array([[0, 1],
                            [1, 0]])

        # Pauli-X mátrix alkalmazása a megadott állapotvektorra és eredmény visszaadása
        return dot(pauli_x, state_vector)

# Pauli-Y kapu osztály
class PauliYGate:
    @staticmethod
    def apply(state_vector):
        # Pauli-Y mátrix definiálása
        pauli_y = np.array([[0, -1j],
                            [1j, 0]])

        # Pauli-Y mátrix alkalmazása az állapotvektorra és eredmény visszaadása
        return dot(pauli_y, state_vector)

# Pauli-Z kapu osztály
class PauliZGate:
    @staticmethod
    def apply(state_vector):
        # Pauli-Z mátrix definiálása
        pauli_z = np.array([[1, 0],
                            [0, -1]])

        # Pauli-Z mátrix alkalmazása az állapotvektorra és eredmény visszaadása
        return dot(pauli_z, state_vector)

# Hadamard kapu osztály
class HadamardGate:
    @staticmethod
    def apply(state_vector):
        # Hadamard mátrix definiálása
        hadamard = sqrt(1 / 2)* np.array([[1, 1],
                                          [1, -1]])

        # Hadamard mátrix alkalmazása az állapotvektorra és az eredmény visszaadása
        return dot(hadamard, state_vector)

# Egyedi kapu osztály
class CustomGate:
    @staticmethod
    def apply(state_vector, multiplier, matrix):
        # Egyedi kapu mátrix definiálása, amely a megadott szorzóval (multiplier) skálázott matrix
        custom_gate = multiplier * matrix

        # Egyedi kapu alkalmazása az állapotvektorra és az eredmény visszaadása
        return dot(custom_gate, state_vector)
