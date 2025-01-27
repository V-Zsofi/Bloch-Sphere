import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure



class BlochSphereCanvas(FigureCanvas):
    def __init__(self, blochsphere):
        # Matplotlib figure és tengelyek inicializálása
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.bloch_sphere = blochsphere
        self.draw_bloch_sphere()
        super().__init__(self.fig)

    #Bloch gömb kirajzolása a vásznon
    def draw_bloch_sphere(self):
        self.axes.cla()
        self.draw_sphere()
        self.draw_axes()
        self.draw_state_vector()
        self.fig.canvas.draw()

    #Gömb felületének kirajzolása
    def draw_sphere(self):
        # gömb grid (hosszúsági és szélességi körök)
        u = np.linspace(0, 2 * np.pi, 100)  # Hosszúsági szög (azimutális)
        v = np.linspace(0, np.pi, 100)  # Szélességi szög (poláris)
        # X, Y, Z koordináták kiszámítása a gömb felületéhez
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))

        # Gömb felületének rajzolása
        self.axes.plot_surface(x, y, z, color='grey', alpha=0.3)

    #Tengelyek, széllességi- és hosszúságikörök kirajzolása
    def draw_axes(self):
        # Középső szélességi kör (ekvátor) az X-Y síkban
        theta = np.linspace(0, 2 * np.pi, 100)
        x_eq = np.cos(theta)
        y_eq = np.sin(theta)
        z_eq = np.zeros_like(theta)
        self.axes.plot(x_eq, y_eq, z_eq, 'grey', lw=2, alpha=0.7)  # Ekvátor kör (szélességi kör)

        # Középső hosszúsági kör az X-Z síkon
        phi = np.linspace(0, 2 * np.pi, 100)
        x_long = np.sin(phi)
        z_long = np.cos(phi)
        y_long = np.zeros_like(phi)
        self.axes.plot(x_long, y_long, z_long, 'grey', lw=2, alpha=0.7)  # Hosszúsági kör az X-Z síkon

        # Középső hosszúsági kör az Y-Z síkon
        self.axes.plot(np.zeros_like(phi), x_long, z_long, 'grey', lw=2, alpha=0.7)  # Hosszúsági kör az Y-Z síkon

        # X, Y, Z tengelyek címkézése és tengelyirányú vektorok rajzolása
        self.axes.quiver(0, 0, 0, 1, 0, 0, color='r', lw=1)  # X tengely
        self.axes.quiver(0, 0, 0, 0, 1, 0, color='g', lw=1)  # Y tengely
        self.axes.quiver(0, 0, 0, 0, 0, 1, color='b', lw=1)  # Z tengely

        # Tengely arányának beállítása egyenlőre az X, Y és Z tengelyeknél
        self.axes.set_box_aspect([1, 1, 1])
        # Nagyobb tengely határok beállítása, hogy a gömb nagyobbnak tűnjön
        self.axes.set_xlim([-0.75, 0.75])
        self.axes.set_ylim([-0.75, 0.75])
        self.axes.set_zlim([-0.75, 0.75])

        # Tengely keretének elrejtése
        self.axes.set_axis_off()

    #Állapot vektor kirajzolása
    def draw_state_vector(self):
        # Állapotvektor rajzolása
        x_vec = np.sin(self.bloch_sphere.alpha) * np.cos(self.bloch_sphere.beta)
        y_vec = np.sin(self.bloch_sphere.alpha) * np.sin(self.bloch_sphere.beta)
        z_vec = np.cos(self.bloch_sphere.alpha)
        self.axes.quiver(0, 0, 0, x_vec, y_vec, z_vec, color='black', lw=3)
        self.axes.scatter(x_vec, y_vec, z_vec, color='red', s=20)

        # Címkék a |0⟩ és |1⟩ állapotokhoz
        self.axes.text(0, 0, 1.1, r'$|0\rangle$', fontsize=15, ha='center')
        self.axes.text(0, 0, -1.3, r'$|1\rangle$', fontsize=15, ha='center')
        self.axes.text(0, 1.05, -0.05, 'Y', fontsize=15)
        self.axes.text(1.05, 0, -0.05, 'X', fontsize=15, ha='right')