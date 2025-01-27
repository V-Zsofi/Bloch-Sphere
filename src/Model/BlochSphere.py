from cmath import phase, cos, exp, sin

from numpy.linalg import norm
from numpy.ma.core import arccos
import numpy as np


# Bloch-gömb osztály definíciója, ami egy kvantumállapotot reprezentál
class BlochSphere:
    def __init__(self):
        # Alapértelmezett poláris szög és fázisszög
        self.alpha = 0    # poláris szög
        self.beta = 0     # fázis szög
        # Kezdeti állapotvektor (|ψ⟩=1|0⟩+0|1⟩, ami |0⟩ állapot)
        self.state_vector = np.array([1.0 + 0j, 0j])

    # Szögek frissítése (alpha és beta) és állapotvektor kiszámítása
    def update_angle(self, alpha, beta):
        # Szögek elmentése
        self.alpha = alpha
        self.beta = beta
        # Állapotvektor újraszámítása a megadott szögekkel
        self.state_vector = np.array([cos(alpha / 2), exp(1j * beta) * sin(alpha / 2)])

    # Állapot frissítése a komplex állapotkomponensekkel (a, b)
    def update_state(self, a, b):
        # Állapotvektor frissítése a komplex számokból
        self.state_vector = np.array([complex(a), complex(b)])
        # Float értékek pontatlansága miatt normálni kell a vektort
        norm_value = norm(self.state_vector)

        if norm_value > 0:  # Ha nem nulla a normálás
            self.state_vector /= norm_value  # Normalizálás

        # Poláris és fázis szögek kiszámítása az új állapotvektor alapján
        norm_a = np.abs(self.state_vector[0])
        norm_a = np.clip(norm_a, -1, 1) # Az arccos függvény érzékenysége és a float pontatlansága miatt
                                               # biztosítani kell hogy a megfelelő intervallumban legyen
        self.alpha = 2 * arccos(norm_a)
        # Fázis szög meghatározása az állapotkomponensekből
        self.beta = phase(b) - phase(a)