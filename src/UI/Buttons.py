from cmath import sqrt

from PyQt5.QtCore import Qt
# A PyQt5 szükséges osztályainak importálása a GUI létrehozásához
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

# Kvantum kapuk importálása a kvantumállapot manipulációjához
from Model.QuantumGate import PauliXGate, PauliYGate, HadamardGate, PauliZGate


# QuantumGateButtons osztály, amely kvantumkapuk GUI-gombjait kezeli
class QuantumGateButtons(QWidget):
    def __init__(self, bloch_sphere_panel, stack_history_panel):
        super().__init__()

        # Hivatkozások a Bloch gömb panelre és a History stack panelre
        self.stack_history_panel = stack_history_panel
        self.bloch_sphere_panel = bloch_sphere_panel

        # Fő elrendezés létrehozása a widgethez
        layout = QVBoxLayout()
        gate_layout = QHBoxLayout()  # Az egyes kvantum kapu gombok vízszintes elrendezése

        # X kapu gomb létrehozása és kattintás esemény összekapcsolása
        self.gate_x = QPushButton("X")
        self.gate_x.clicked.connect(self.pauli_x_apply)

        # Y kapu gomb létrehozása és kattintás esemény összekapcsolása
        self.gate_y = QPushButton("Y")
        self.gate_y.clicked.connect(self.pauli_y_apply)

        # Z kapu gomb létrehozása és kattintás esemény összekapcsolása
        self.gate_z = QPushButton("Z")
        self.gate_z.clicked.connect(self.pauli_z_apply)

        # H (Hadamard) kapu gomb létrehozása és kattintás esemény összekapcsolása
        self.gate_h = QPushButton("H")
        self.gate_h.clicked.connect(self.hadamard_apply)

        # Gombok hozzáadása a gate_layout elrendezéshez
        gate_layout.addWidget(self.gate_x)
        gate_layout.addWidget(self.gate_y)
        gate_layout.addWidget(self.gate_z)
        gate_layout.addWidget(self.gate_h)

        # Címke és elrendezések hozzáadása a fő elrendezéshez
        layout.addWidget(QLabel("Quantum Gates"))
        layout.addLayout(gate_layout)
        self.setLayout(layout)

    # Pauli-X kapu alkalmazása az aktuális kvantumállapotra
    def pauli_x_apply(self):
        bloch_sphere = self.bloch_sphere_panel.bloch_sphere
        new_state = PauliXGate.apply(bloch_sphere.state_vector) # Pauli X kapu alkalmazása
        bloch_sphere.update_state(new_state[0], new_state[1]) # Állapot vektor frissítése

        # Művelet naplózása a stack history panel segítségével
        self.stack_history_panel.history_list.log_change("Pauli X gate applied.", new_state[0], new_state[1])
        self.stack_history_panel.update_history_display()
        self.bloch_sphere_panel.update_bloch_sphere() # Bloch gömb megjelenítés frissítése

    # Pauli-Y kapu alkalmazása az aktuális kvantumállapotra
    def pauli_y_apply(self):
        bloch_sphere = self.bloch_sphere_panel.bloch_sphere
        new_state = PauliYGate.apply(bloch_sphere.state_vector) # Pauli Y kapu alkalmazása
        bloch_sphere.update_state(new_state[0], new_state[1]) # Állapot vektor frissítése

        # Művelet naplózása a stack history panel segítségével
        self.stack_history_panel.history_list.log_change("Pauli Y gate applied.", new_state[0], new_state[1])
        self.stack_history_panel.update_history_display()
        self.bloch_sphere_panel.update_bloch_sphere() # Bloch gömb megjelenítés frissítése

    # Pauli-Z kapu alkalmazása az aktuális kvantumállapotra
    def pauli_z_apply(self):
        bloch_sphere = self.bloch_sphere_panel.bloch_sphere
        new_state = PauliZGate.apply(bloch_sphere.state_vector) # Pauli Z kapu alkalmazása
        bloch_sphere.update_state(new_state[0], new_state[1]) # Állapot vektor frissítése

        # Művelet naplózása a stack history panel segítségével
        self.stack_history_panel.history_list.log_change("Pauli Z gate applied.", new_state[0], new_state[1])
        self.stack_history_panel.update_history_display()
        self.bloch_sphere_panel.update_bloch_sphere() # Bloch gömb megjelenítés frissítése

    # Hadamard kapu alkalmazása az aktuális kvantumállapotra
    def hadamard_apply(self):
        bloch_sphere = self.bloch_sphere_panel.bloch_sphere
        new_state = HadamardGate.apply(bloch_sphere.state_vector) # Hadamard kapu alkalmazása
        bloch_sphere.update_state(new_state[0], new_state[1]) # Állapot vektor frissítése

        # Művelet naplózása a stack history panel segítségével
        self.stack_history_panel.history_list.log_change("Hadamard gate applied.", new_state[0], new_state[1])
        self.stack_history_panel.update_history_display()
        self.bloch_sphere_panel.update_bloch_sphere() # Bloch gömb megjelenítés frissítése


# Állapotválasztó gombokat kezelő osztály
class StateSelectionButtons(QWidget):
    def __init__(self, bloch_sphere_panel, stack_history_panel):
        super().__init__()

        # Hivatkozások a Bloch gömb panelre és a History Stack panelre
        self.stack_history_panel = stack_history_panel
        self.bloch_sphere_panel = bloch_sphere_panel

        # Gombok elrendezése
        button_layout = QHBoxLayout()
        undo_layout = QHBoxLayout()
        state_selection_layout = QVBoxLayout()

        # Állapot kiválasztó gombok létrehozása és kattintás esemény összekapcsolása
        self.state_0 = QPushButton("|0⟩")
        self.state_0.clicked.connect(self.state_0_apply)

        self.state_1 = QPushButton("|1⟩")
        self.state_1.clicked.connect(self.state_1_apply)

        self.state_minus = QPushButton("|−⟩")
        self.state_minus.clicked.connect(self.state_minus_apply)

        self.state_plus = QPushButton("|+⟩")
        self.state_plus.clicked.connect(self.state_plus_apply)

        # Visszavonás gomb létrehozása és kattintás esemény összekapcsolása
        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo_step)

        # Init gomb, ami törli az összes eddigi változtatást és visszaáll alap állapotba
        self.init_button = QPushButton("Init")
        self.init_button.clicked.connect(self.init_step)

        # Gombok hozzáadása az elrendezésekhez
        button_layout.addWidget(self.state_0)
        button_layout.addWidget(self.state_1)
        button_layout.addWidget(self.state_minus)
        button_layout.addWidget(self.state_plus)
        state_selection_layout.addLayout(button_layout)
        undo_layout.addWidget(self.undo_button, alignment= Qt.AlignRight)
        undo_layout.addWidget(self.init_button, alignment= Qt.AlignLeft) # Középen látszodjanak a gombok
        state_selection_layout.addLayout(undo_layout)

        self.setLayout(state_selection_layout)

    # Állapot beállítása |0⟩ állapotra
    def state_0_apply(self):
        bloch_sphere = self.bloch_sphere_panel.bloch_sphere
        bloch_sphere.update_state(1, 0) # Állapot vektor beállítása

        # Naplózás a stack history panel segítségével
        self.stack_history_panel.history_list.log_change("State |0⟩ applied.", 1, 0)
        self.stack_history_panel.update_history_display()
        self.bloch_sphere_panel.update_bloch_sphere() # Bloch gömb megjelenítés frissítése

    # Állapot beállítása |1⟩ állapotra
    def state_1_apply(self):
        bloch_sphere = self.bloch_sphere_panel.bloch_sphere
        bloch_sphere.update_state(0, 1) # Állapot vektor beállítása

        # Naplózás a stack history panel segítségével
        self.stack_history_panel.history_list.log_change("State |1⟩ applied.", 0, 1)
        self.stack_history_panel.update_history_display()
        self.bloch_sphere_panel.update_bloch_sphere() # Bloch gömb megjelenítés frissítése

    # Állapot beállítása |−⟩ állapotra
    def state_minus_apply(self):
        bloch_sphere = self.bloch_sphere_panel.bloch_sphere
        bloch_sphere.update_state(sqrt(1 / 2), -1.0 * sqrt(1 / 2)) # Állapot vektor beállítása

        # Naplózás a stack history panel segítségével
        self.stack_history_panel.history_list.log_change("State |-⟩ applied.", sqrt(1 / 2), -1 * sqrt(1 / 2))
        self.stack_history_panel.update_history_display()
        self.bloch_sphere_panel.update_bloch_sphere() # Bloch gömb megjelenítés frissítése

    # Állapot beállítása |+⟩ állapotra
    def state_plus_apply(self):
        bloch_sphere = self.bloch_sphere_panel.bloch_sphere
        bloch_sphere.update_state(sqrt(1 / 2), sqrt(1 / 2)) # Állapot vektor beállítása

        # Naplózás a stack history panel segítségével
        self.stack_history_panel.history_list.log_change("State |+⟩ applied.", sqrt(1 / 2), sqrt(1 / 2))
        self.stack_history_panel.update_history_display()
        self.bloch_sphere_panel.update_bloch_sphere()  # Bloch gömb megjelenítés frissítése

    # Utolsó művelet visszavonása
    def undo_step(self):
        self.stack_history_panel.history_list.undo_change()
        self.stack_history_panel.update_history_display()

    # Összes művelet törlése
    def init_step(self):
        self.stack_history_panel.history_list.delete_all()
        self.stack_history_panel.update_history_display()