import sys

from PyQt5.QtWidgets import QApplication

from UI.UIManager import UIManager


# Az QApplication objektum létrehozása, amely a PyQt5 alkalmazás alapját képezi
app = QApplication(sys.argv)
# Az UIManager példányának létrehozása, amely a fő ablakot képviseli
window = UIManager()
# Az ablak megjelenítése
window.show()
# Az alkalmazás futtatása; ha az ablak bezárul, a program kilép
sys.exit(app.exec_())