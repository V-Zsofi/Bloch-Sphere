from PyQt5.QtGui import QFont, QTextBlockFormat
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel

# StackHistoryPanel osztály, amely megjeleníti a kvantumállapotokon végzett műveleteket
class StackHistoryPanel(QWidget):
    def __init__(self, history):
        super().__init__()
        self.history_list = history  # A módosítási lista tárolása
        layout = QVBoxLayout()  # Fő elrendezés létrehozása

        # Címke létrehozása a módosítások számára
        layout.addWidget(QLabel("Stack History"))

        # QTextEdit létrehozása a módosítások megjelenítéséhez
        self.stack_history = QTextEdit()
        self.stack_history.setReadOnly(True)  # Csak olvasható, a felhasználó nem módosíthatja

        # Betűtípus beállítása (nagyítása/kicsinyítése)
        font = QFont()
        font.setPointSize(12)  # Betűméret beállítása (10-es méret)

        # Betűtípus alkalmazása a QTextEdit-re
        self.stack_history.setFont(font)

        # QTextEdit hozzáadása az elrendezéshez
        layout.addWidget(self.stack_history)
        self.setLayout(layout)  # Az elrendezés beállítása a widgethez

        self.update_history_display()  # A módosítások megjelenítésének frissítése

    def update_history_display(self):
        # Az utolsó öt változás összegyűjtése és új sorokkal való összekapcsolása
        history_text = "\n\n".join(self.history_list.get_last_five_changes())  # módosítási elemek összefűzése
        self.stack_history.setPlainText(history_text)  # A szöveg beállítása a QTextEdit-ben
