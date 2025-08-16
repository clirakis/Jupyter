"""
IsingModel.py

Modified    By    Reason
30-Jun-25   CBL   taken from reference below.
01-Jul-25   CBL   Looks like PyQt implementation is a bit old. 

References:
https://github.com/ddatsko/3d-ising-model/blob/master/IsingModel3d.py

Changes going to Qt6
https://pyqtgraph.readthedocs.io/en/latest/getting_started/how_to_use.html

"""
from IsingModel import IsingModel
import pyqtgraph.Qt as pyqt
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
from typing import Iterable
import sys


class IsingModel3d(IsingModel):
    RED = (1, 0.1, 0.1, 0.1)
    BLUE = (0.1, 0.1, 1, 0.1)

    def __init__(self, x_size: int, y_size: int, z_size: int, temperature: float, interaction: float,
                 initializer: callable((int, int, int)) = lambda x, y, z: 1, sphere_radius: float = 0.2):
        super().__init__(x_size, y_size, z_size, temperature, interaction, initializer)
        self.sphere_radius = sphere_radius
        #self.app = QtGui.QApplication(sys.argv) Original
        # CBL This makes the application work, but the UI is never
        # visualized. 
        self.app = pyqt.mkQApp(sys.argv[0])
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 40
        self.w.setWindowTitle('Ising Model')
        self.w.setGeometry(0, 50, 1920, 1080)

        # Create a grid on the sides of the model
        # gx = gl.GLGridItem(size=QtGui.QVector3D(y_size, z_size, 1))
        # gx.rotate(90, 0, 1, 0)
        # gx.translate(-x_size / 2, 0, 0)
        # self.w.addItem(gx)
        # gy = gl.GLGridItem(size=QtGui.QVector3D(x_size, z_size, 1))
        # gy.rotate(90, 1, 0, 0)
        # gy.translate(0, -y_size / 2, 0)
        # self.w.addItem(gy)
        # gz = gl.GLGridItem(size=QtGui.QVector3D(x_size, y_size, 1))
        # gz.translate(0, 0, -z_size / 2)
        # self.w.addItem(gz)

        self.points = []
        for i in range(self.x_size):
            self.points.append([])
            for j in range(self.y_size):
                self.points[i].append([])
                for k in range(self.z_size):
                    sphere_color = IsingModel3d.RED if self.particles[i][j][k] == -1 else IsingModel3d.BLUE
                    sphere = self.create_sphere(sphere_color, (i, j, k))
                    self.points[i][j].append(sphere)
                    self.w.addItem(sphere)

    def create_sphere(self, color: tuple[float, float, float, float], position: tuple[int, int, int]) -> gl.GLMeshItem:
        sphere = gl.MeshData.sphere(4, 4, radius=self.sphere_radius)
        item = gl.GLMeshItem(meshdata=sphere, smooth=False, color=color, shader='balloon', glOptions='additive')
        item.translate(*position)
        return item

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            # This is old
            #QtGui.QApplication.instance().exec_()
            self.app.exec()
            
    def update_points(self):
        for i in range(self.x_size):
            for j in range(self.y_size):
                for k in range(self.z_size):
                    self.points[i][j][k].setColor(
                        IsingModel3d.RED if self.particles[i][j][k] == -1 else IsingModel3d.BLUE)

    def make_visualized_step(self):
        print('step')
        self.make_simulation_step()
        self.update()

    def run_simulation(self, n_max: int, simulations_per_temperature: int = 10, generate_graphs: bool = True,
                       visualize: bool = False,
                       temperatures_list: Iterable[float] = ()):
        if visualize:
            self.w.show()
            timer = QtCore.QTimer()
            timer.timeout.connect(self.make_visualized_step)
            timer.start(100)
            self.start()
            return
        else:
            super().run_simulation(n_max, simulations_per_temperature, generate_graphs, temperatures_list)

    def update(self):
        self.update_points()
