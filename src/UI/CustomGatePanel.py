import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from numpy import dot
from sympy import sympify

from Model.QuantumGate import CustomGate


def convert_to_complex(input_str):
    #Segédfüggvény, amely átalakítja a bemenetet komplex számokká, biztosítva, hogy ha csak 'j' szerepel,
    #akkor hibaüzenet jelenjen meg.
    input_str = input_str.strip()  # Eltávolítjuk a fölösleges szóközöket
    if input_str == 'j' or input_str == '-j':  # Ha csak 'j' vagy '-j' van, akkor hibát dobunk
        raise ValueError("Invalid complex number format: Missing coefficient for 'j'.")

    try:
        # Próbáljuk szimpatikus formába alakítani és komplex számot készíteni
        return complex(sympify(input_str))
    except Exception:
        # Ha nem sikerül, hibát jelezünk
        raise ValueError("Invalid complex number format")


class CustomGatesPanel(QWidget):
    def __init__(self, bloch_sphere_panel, stack_history_panel):
        super().__init__()

        # Fő elrendezés létrehozása a widget számára
        layout = QVBoxLayout()
        custom_grid = QGridLayout()  # Egyedi mátrixbeviteli mezők elrendezése
        self.stack_history_panel = stack_history_panel
        self.bloch_sphere_panel = bloch_sphere_panel

        # Címke hozzáadása az egyedi kvantumkapuk szekcióhoz
        custom_grid.addWidget(QLabel("Custom Quantum Gates"), 0, 0, 1, 2)

        # Mátrixelemek beviteléhez szükséges mezők létrehozása
        self.matrix_input_1 = QLineEdit()
        self.matrix_input_1.setPlaceholderText("m1")  # Helykitöltő szöveg beállítása a mezőben
        self.matrix_input_2 = QLineEdit()
        self.matrix_input_2.setPlaceholderText("m2") # Helykitöltő szöveg beállítása a mezőben
        self.matrix_input_3 = QLineEdit()
        self.matrix_input_3.setPlaceholderText("m3") # Helykitöltő szöveg beállítása a mezőben
        self.matrix_input_4 = QLineEdit()
        self.matrix_input_4.setPlaceholderText("m4") # Helykitöltő szöveg beállítása a mezőben

        # A mezők elhelyezése a grid elrendezésben
        custom_grid.addWidget(self.matrix_input_1, 1, 1)
        custom_grid.addWidget(self.matrix_input_2, 1, 2)
        custom_grid.addWidget(self.matrix_input_3, 3, 1)
        custom_grid.addWidget(self.matrix_input_4, 3, 2)

        # Szorzó (multiplier) beviteléhez szükséges mező létrehozása
        self.multiplier_input = QLineEdit()
        self.multiplier_input.setPlaceholderText("multiplier")  # Helykitöltő szöveg beállítása a mezőben
        custom_grid.addWidget(self.multiplier_input, 2, 0)

        # Az elrendezés hozzáadása a fő elrendezéshez
        layout.addLayout(custom_grid)

        # "Apply" gomb létrehozása és kattintás esemény összekapcsolása
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_custom_gates)
        layout.addWidget(self.apply_button, alignment=Qt.AlignCenter)  # Gomb középre igazítása
        self.setLayout(layout)

    # Egyedi kapu alkalmazásához szükséges függvény
    def apply_custom_gates(self):
        # Felhasználói bevitel lekérése a mátrix elemeihez és a szorzóhoz
        try:
            # Felhasználói inputok kinyerése
            m1 = convert_to_complex(self.matrix_input_1.text())
            m2 = convert_to_complex(self.matrix_input_2.text())
            m3 = convert_to_complex(self.matrix_input_3.text())
            m4 = convert_to_complex(self.matrix_input_4.text())

            # Ha nincs szorzó megadva, alapértelmezettként 1-et használ
            multiplier = float(sympify(self.multiplier_input.text())) if self.multiplier_input.text() else 1

            # A mátrix összeállítása a felhasználó által megadott elemekkel és szorzóval
            matrix = multiplier * np.array([[m1, m2],
                                            [m3, m4]])

            # Ellenőrzés, hogy a mátrix unitér-e (feltétel a kvantum kapuk számára)
            if not np.allclose(np.eye(matrix.shape[0]), dot(matrix, matrix.conj().T)):
                # Hibajelzés, ha a mátrix nem unitér
                QMessageBox.warning(self, "Error", "The given matrix is not unitary.")
                return

            # Egyedi kapu alkalmazása a Bloch-szférán
            bloch_sphere = self.bloch_sphere_panel.bloch_sphere
            new_state = CustomGate.apply(bloch_sphere.state_vector, multiplier, np.array([[m1, m2],[m3, m4]]))
            # Bloch gömb frissítése az új állapot alapján
            bloch_sphere.update_state(new_state[0], new_state[1])
            self.bloch_sphere_panel.update_bloch_sphere()

            # Az esemény naplózása a stack history panel segítségével
            self.stack_history_panel.history_list.log_change("Custom gate applied", new_state[0], new_state[1])
            self.stack_history_panel.update_history_display()

        # Hibakezelés: ha nem megfelelő a bevitel, figyelmeztetés jelenik meg
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))