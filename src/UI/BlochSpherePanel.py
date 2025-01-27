from numpy import isclose

# PyQt5 könyvtárak és osztályok importálása a GUI létrehozásához
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox
from sympy import sympify

# Bloch gömb modellek importálása
from Model.BlochSphere import BlochSphere
from UI.BlochSphereCanvas import BlochSphereCanvas
from UI.CustomGatePanel import convert_to_complex


# BlochSpherePanel osztály, amely a Bloch gömb és az állapot megjelenítést kezeli
class BlochSpherePanel(QWidget):
    def __init__(self, alpha_beta_slider, stack_history_panel):
        # Szülő QWidget inicializálása
        super().__init__()

        # Hivatkozás tárolása az AlphaBetaSlider és a StackHistoryPanel osztályokra
        self.alpha_beta_slider = alpha_beta_slider
        self.stack_history_panel = stack_history_panel

        # Fő elrendezés létrehozása a widgethez
        layout = QVBoxLayout()

        # Bloch gömb objektum létrehozása és a Bloch gömb vászon inicializálása
        self.bloch_sphere = BlochSphere()
        self.bloch_sphere_canvas = BlochSphereCanvas(self.bloch_sphere)

        # Bloch gömb vászon hozzáadása az elrendezéshez
        layout.addWidget(self.bloch_sphere_canvas)

        # Állapot input megjelenítés elrendezése
        state_layout = QHBoxLayout()

        # QLineEdit mező létrehozása az 'a' értékhez és beállítása
        self.a_line_edit = QLineEdit()
        self.a_line_edit.setPlaceholderText("Enter value for a")  # Segédszöveg beállítása
        # QLineEdit mező létrehozása a 'b' értékhez és beállítása
        self.b_line_edit = QLineEdit()
        self.b_line_edit.setPlaceholderText("Enter value for b")  # Segédszöveg beállítása

        # Állapot input megjelenítő elemek hozzáadása az elrendezéshez
        state_layout.addWidget(self.a_line_edit)
        state_layout.addWidget(QLabel("|0⟩ + "))
        state_layout.addWidget(self.b_line_edit)
        state_layout.addWidget(QLabel("|1⟩"))

        # Az apply gomb létrehozása és eseménykezelő összekapcsolása
        self.apply_button = QPushButton("Apply")
        self.apply_button.setFixedWidth(80)  # Gomb szélességének beállítása
        self.apply_button.clicked.connect(self.apply_state)  # Klikkelési esemény kapcsolása

        # Gomb hozzáadása az állapot input elrendezéshez
        state_layout.addWidget(self.apply_button)

        # Az állapot elrendezés hozzáadása a fő elrendezéshez
        layout.addLayout(state_layout)

        # Fő elrendezés beállítása a widgethez
        self.setLayout(layout)

    # Bloch gömb megjelenítésének frissítése
    def update_bloch_sphere(self):
        # Szögcsúszkák frissítése az AlphaBetaSlider segítségével
        self.alpha_beta_slider.update_sliders()

        # Bloch gömb újrarajzolása
        self.bloch_sphere_canvas.draw_bloch_sphere()
        self.bloch_sphere_canvas.flush_events()

    # Állapot alkalmazása a felhasználó által megadott értékek alapján
    def apply_state(self):
        # 'a' és 'b' mezők szövegének lekérése
        a_text = self.a_line_edit.text()
        b_text = self.b_line_edit.text()

        try:
            # Ha az 'a' mező üres, értéke legyen 0, különben konvertálás complex típusra
            a = convert_to_complex(a_text) if a_text else 0
            # Ha a 'b' mező üres, értéke legyen 0, különben konvertálás complex típusra
            b = convert_to_complex(b_text) if b_text else 0
        except ValueError as e:
            # Hibaüzenet megjelenítése, ha a kifejezés nem értelmezhető
            QMessageBox.warning(self, "Invalid Expression", str(e))
            return  # Kilépés a metódusból, ha az érték nem megfelelő

        # Normál érték kiszámítása a kvantum állapot érvényességének ellenőrzéséhez
        norm = abs(a) ** 2 + abs(b) ** 2

        # Ha az összeg nem egyenlő 1-el, akkor hibaüzenet megjelenítése
        if not isclose(norm, 1.0):
            QMessageBox.warning(self, "Invalid State",
                        "The value of |a|^2 + |b|^2 is not equal to 1. "
                        "Please provide valid values for the qubit state.")
            return  # Kilépés a metódusból, ha az érték nem megfelelő

        # Bloch gömb állapotának frissítése az 'a' és 'b' értékekkel
        self.bloch_sphere.update_state(a, b)

        # Naplózás a StackHistoryPanel segítségével
        self.stack_history_panel.history_list.log_change(
            f"State value changed to {a_text.replace('\n', '')}|0⟩+{b_text.replace('\n', '')}|1⟩.", a, b
        )

        # Napló megjelenítés frissítése
        self.stack_history_panel.update_history_display()

        # Bloch gömb megjelenítő frissítése
        self.update_bloch_sphere()
