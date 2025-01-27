from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout)

from Model.StackHistory import StackHistory
from UI.BlochSpherePanel import BlochSpherePanel
from UI.Buttons import QuantumGateButtons, StateSelectionButtons
from UI.CustomGatePanel import CustomGatesPanel
from UI.AlphaBetaSlider import AlphaBetaSlider
from UI.StackHistoryPanel import StackHistoryPanel

# UIManager osztály, amely kezeli a Bloch gömb szimulátor felhasználói felületét
class UIManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Bloch Sphere Simulator')  # Az ablak címe
        self.setGeometry(100, 100, 1200, 800)  # Az ablak pozíciója és mérete
        self.setFixedSize(1200, 800)  # Az ablak méretének rögzítése, a felhazsnáló nem állíthatja át másikra

        main_layout = QHBoxLayout()  # Fő elrendezés létrehozása vízszintesen

        self.history = StackHistory(None)  # StackHistory objektum létrehozása
        self.stack_history_panel = StackHistoryPanel(self.history)  # StackHistoryPanel létrehozása

        # Bal panel
        left_layout = QVBoxLayout()  # Bal oldali elrendezés létrehozása függőlegesen
        self.alpha_beta_panel = AlphaBetaSlider(None, self.stack_history_panel)  # AlphaBetaSlider létrehozása
        self.bloch_sphere_panel = BlochSpherePanel(self.alpha_beta_panel, self.stack_history_panel)  # BlochSpherePanel létrehozása
        self.history.bloch_sphere_panel = self.bloch_sphere_panel  # Kapcsolat létrehozása a Stack History és a Bloch gömb között
        self.alpha_beta_panel.bloch_sphere_panel = self.bloch_sphere_panel  # Kétirányú kapcsolat a panelek között
        left_layout.addWidget(self.bloch_sphere_panel)  # Bloch gömb hozzáadása a bal panelhez
        left_layout.addWidget(self.alpha_beta_panel)  # Alpha-beta panel hozzáadása a bal panelhez

        left_widget = QWidget()  # Bal widget létrehozása
        left_widget.setLayout(left_layout)  # Az elrendezés beállítása a widgethez

        # Jobb panel
        right_layout = QVBoxLayout()  # Jobb oldali elrendezés létrehozása függőlegesen
        self.quantum_gates_panel = QuantumGateButtons(self.bloch_sphere_panel, self.stack_history_panel)  # Kvantumkapu gombok létrehozása
        self.custom_gates_panel = CustomGatesPanel(self.bloch_sphere_panel, self.stack_history_panel)  # Egyéni kapuk panel létrehozása
        self.state_selection_panel = StateSelectionButtons(self.bloch_sphere_panel, self.stack_history_panel)  # Állapotválasztó gombok létrehozása

        right_layout.addWidget(self.quantum_gates_panel)  # Kvantumkapu panel hozzáadása a jobb panelhez
        right_layout.addWidget(self.custom_gates_panel)  # Egyéni kapu panel hozzáadása a jobb panelhez
        right_layout.addWidget(self.stack_history_panel)  # History Stack panel hozzáadása a jobb panelhez
        right_layout.addWidget(self.state_selection_panel)  # Állapotválasztó panel hozzáadása a jobb panelhez

        right_widget = QWidget()  # Jobb widget létrehozása
        right_widget.setLayout(right_layout)  # Az elrendezés beállítása a widgethez

        # Fő elrendezés
        main_layout.addWidget(left_widget)  # Bal widget hozzáadása a fő elrendezéshez
        main_layout.addWidget(right_widget)  # Jobb widget hozzáadása a fő elrendezéshez

        container = QWidget()  # Konténer widget létrehozása
        container.setLayout(main_layout)  # Az elrendezés beállítása a konténerhez
        self.setCentralWidget(container)  # A konténer beállítása középponti widgetként
