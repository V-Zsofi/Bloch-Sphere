from sympy import sympify

# StackHistory osztály, ami az állapotváltozások naplózását és visszavonását kezeli
class StackHistory:
    def __init__(self, bloch_sphere_panel):
        # Naplófájl neve, ahová az állapotváltozásokat rögzítjük
        self.file_name = "History_log.txt"
        # Hivatkozás a Bloch-szféra panelre, amely vizualizálja az állapotot
        self.bloch_sphere_panel = bloch_sphere_panel
        # A fájl megnyitása törlésre, hogy csak az új változások kerüljenek bele, korábbi leírások nélkül
        open(self.file_name, "w+", encoding="utf-8").close()

    # Az utolsó öt változtatás lekérdezése
    def get_last_five_changes(self):
        #sorok kiolvasása a fájlból
        with open(self.file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Minden sor feldolgozása csak az üzenet rész megtartásához (a két utolsó tabbal elválasztott szám elhagyása)
        last_five_changes = []
        for line in lines[-5:]:  # Csak az utolsó 5 sor feldolgozása
            parts = line.strip().split('\t')  # Sor szétválasztása tabulátor mentén
            message = parts[0]  # Az üzenet részének kinyerése (minden, ami a számok előtt van)
            last_five_changes.append(message)

        return last_five_changes

    # Új változtatás rögzítése a naplófájlba
    def log_change(self, change_description, a_value, b_value):
        # A változtatás leírása és az értékek helyes formátumba alakítása
        formatted_description = f"{change_description}\t{a_value}\t{b_value}"

        # Új sor hozzáadása a naplófájlhoz
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(formatted_description + "\n")

    # Legutóbbi változtatás visszavonása
    def undo_change(self):
        # Fájl megnyitása olvasásra, sorok beolvasása
        with open(self.file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Ha a fájl üres, nincs mit visszavonni
        if len(lines) == 0:
            return

        # Ha csak egyetlen sor van, töröljük azt, és visszaállítjuk az alapállapotot |0⟩
        if len(lines) == 1:
            lines.pop()  # Az utolsó sor eltávolítása
            # Bloch gömb visszaállítása |0⟩ állapotra (1, 0)
            self.bloch_sphere_panel.bloch_sphere.update_state(1, 0)
            self.bloch_sphere_panel.update_bloch_sphere()
            # Fájl felülírása az üres sorokkal
            with open(self.file_name, "w", encoding="utf-8") as file:
                file.writelines(lines)
            return

        # Második legutolsó sor kiválasztása
        second_to_last_line = lines[-2].strip()
        lines.pop()  # Utolsó sor eltávolítása

        # Második legutolsó sor felosztása tabulátorok mentén az értékek kinyeréséhez
        parts = second_to_last_line.split('\t')

        # Az utolsó előtti értékek a, b konvertálása komplex számokká
        a = complex(sympify(parts[-2]))  # Utolsó előtti elem (a érték)
        b = complex(sympify(parts[-1]))  # Utolsó elem (b érték)

        # Bloch gömb állapotának frissítése a visszavont a és b értékek alapján
        self.bloch_sphere_panel.bloch_sphere.update_state(a, b)
        self.bloch_sphere_panel.update_bloch_sphere()

        # Fájl felülírása a maradék sorokkal (az utolsó sor nélkül)
        with open(self.file_name, "w", encoding="utf-8") as file:
            file.writelines(lines)

    def delete_all(self):
        with open(self.file_name, "w", encoding="utf-8") as file:
            file.writelines("")

        self.bloch_sphere_panel.bloch_sphere.update_state(1, 0)
        self.bloch_sphere_panel.update_bloch_sphere()