from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QSlider, QLabel, QPushButton, QHBoxLayout
import math


# AlphaBetaSlider osztály, amely egy grafikus felületet biztosít a Bloch-gömb forgatási szögének állítására
class AlphaBetaSlider(QWidget):
    def __init__(self, bloch_sphere_panel, stack_history_panel):
        # Szülőosztály inicializálása
        super().__init__()
        # StackHistoryPanel-re és a BlochSpherePanel-re való hivatkozások mentése
        self.stack_history_panel = stack_history_panel
        self.bloch_sphere_panel = bloch_sphere_panel

        # Függőleges elrendezés létrehozása
        layout = QVBoxLayout()

        # Alpha szög vezérlői
        self.alpha_slider = QSlider(Qt.Horizontal)  # Vízszintes csúszka létrehozása
        self.alpha_slider.setRange(0, int(math.pi * 100))  # Értéktartomány 0 és π között 100-as szorzással
        self.alpha_slider.valueChanged.connect(self.update_alpha_value)  # Frissítés hívása, ha az érték változik
        self.alpha_slider.sliderReleased.connect(self.alpha_logger)  # Logoló hívása, ha elengedik a csúszkát
        self.alpha_value_label = QLabel("Alpha (0.0 rad):")  # Kezdeti címke az Alpha érték megjelenítéséhez

        # Alpha csúszka és címke hozzáadása az elrendezéshez
        layout.addWidget(self.alpha_value_label)
        layout.addWidget(self.alpha_slider)

        # Beta szög vezérlői
        self.beta_slider = QSlider(Qt.Horizontal)  # Vízszintes csúszka létrehozása a Beta értékhez
        self.beta_slider.setRange(0, int(2 * math.pi * 100))  # Értéktartomány 0 és 2π között 100-as szorzással
        self.beta_slider.valueChanged.connect(self.update_beta_value)  # Frissítés hívása, ha az érték változik
        self.beta_slider.sliderReleased.connect(self.beta_logger)  # Logoló hívása, ha elengedik a csúszkát
        self.beta_value_label = QLabel("Beta (0.0 rad):")  # Kezdeti címke a Beta érték megjelenítéséhez

        # Beta csúszka és címke hozzáadása az elrendezéshez
        layout.addWidget(self.beta_value_label)
        layout.addWidget(self.beta_slider)

        # Az elrendezés beállítása a widgethez
        self.setLayout(layout)

    # Az Alpha érték frissítése a csúszka állásából
    def update_alpha_value(self):
        # Alpha szög kiszámítása a csúszka pozíciójából és a címke frissítése
        alpha = self.alpha_slider.value() / (math.pi * 100) * math.pi
        self.alpha_value_label.setText(f"Alpha ({alpha:.2f} rad):")

        # Alpha szög beállítása a Bloch gömb panelen, majd annak frissítése
        self.bloch_sphere_panel.bloch_sphere.update_angle(alpha, self.bloch_sphere_panel.bloch_sphere.beta)
        self.bloch_sphere_panel.update_bloch_sphere()

    # A Beta érték frissítése a csúszka állásából
    def update_beta_value(self):
        # Beta szög kiszámítása a csúszka pozíciójából és a címke frissítése
        beta = self.beta_slider.value() / (math.pi * 100) * math.pi
        self.beta_value_label.setText(f"Beta ({beta:.2f} rad):")

        # Beta szög beállítása a Bloch gömb panelen, majd annak frissítése
        self.bloch_sphere_panel.bloch_sphere.update_angle(self.bloch_sphere_panel.bloch_sphere.alpha, beta)
        self.bloch_sphere_panel.update_bloch_sphere()

    # Csúszkák frissítése az aktuális szögek szerint
    def update_sliders(self):
        # Blockolni kell az setValue hívás miatt, hogy ne hívja meg az update függvényeket
        self.alpha_slider.blockSignals(True)
        self.beta_slider.blockSignals(True)

        # Alpha csúszka pozíciójának kiszámítása az aktuális Alpha érték alapján
        alpha_slider_value = int((self.bloch_sphere_panel.bloch_sphere.alpha / math.pi) * (math.pi * 100))
        self.alpha_slider.setValue(alpha_slider_value)
        self.alpha_value_label.setText(f"Alpha ({self.bloch_sphere_panel.bloch_sphere.alpha:.2f} rad):")

        beta_value = self.bloch_sphere_panel.bloch_sphere.beta
        if beta_value < 0:
            beta_value += 2 * math.pi
        # Beta csúszka pozíciójának kiszámítása az aktuális Beta érték alapján
        beta_slider_value = int((beta_value / (2 * math.pi)) * (2 * math.pi * 100))
        self.beta_slider.setValue(beta_slider_value)
        self.beta_value_label.setText(f"Beta ({beta_value:.2f} rad):")

        # Block leállítása
        self.alpha_slider.blockSignals(False)
        self.beta_slider.blockSignals(False)

    # Alpha változás logolása
    def alpha_logger(self):
        # Aktuális állapotvektor lekérése
        state_vector = self.bloch_sphere_panel.bloch_sphere.state_vector
        # Alpha változás rögzítése a naplófájlba
        self.stack_history_panel.history_list.log_change("Alpha value changed.", state_vector[0], state_vector[1])
        # Napló megjelenítésének frissítése
        self.stack_history_panel.update_history_display()

    # Beta változás logolása
    def beta_logger(self):
        # Aktuális állapotvektor lekérése
        state_vector = self.bloch_sphere_panel.bloch_sphere.state_vector
        # Beta változás rögzítése a naplófájlba
        self.stack_history_panel.history_list.log_change("Beta value changed.", state_vector[0], state_vector[1])
        # Napló megjelenítésének frissítése
        self.stack_history_panel.update_history_display()
