from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from PyQt5.QtGui import QFont
from form import *
import sys
import shooting as sh
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Window(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.set_values.clicked.connect(self.Set_data)
        self.clear_.clicked.connect(self.clear)

        # -- график --
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.figure = Figure()
        self.axes = self.figure.gca()
        self.axes.set_title("plot")

    def __data(self):
        self.d = [
            str(self.f1_input.text()),
            str(self.f2_input.text()),
            float(self.x0_input.text()),
            [float(self.nu1_input.text()), float(self.nu2_input.text())],
            float(self.alp0_input.text()),
            float(self.bet0_input.text()),
            float(self.alp1_input.text()),
            float(self.bet1_input.text()),
            float(self.A_input.text()),
            float(self.B_input.text()),
            int(self.a_input.text()),
            int(self.b_input.text()),
        ]
        if self.accur_input.text() == "":
            self.accur = 2
        else:
            self.accur = int(self.accur_input.text())
        print(self.d, self.accur)

    def Set_data(self):
        self.__data()
        self.obj = sh.Shooting(*self.d, accuracy = self.accur)
        self.f = self.obj.Requirement()
        self.req.setText(self.f)
        self.req.setFont(QFont('Arial', 22))
        self.k, self.v = self.obj.Data()
        self.graph()
        print(self.obj.Start())

    def graph(self):
        self.axes.clear()
        self.axes.plot(self.k, self.v, "green")

        self.axes.legend(["trajectory"])
        self.axes.grid(True)

        self.canvas = FigureCanvas(self.figure)
        self.proxy_widget = self.scene.addWidget(self.canvas)

    def clear(self):
        self.k.clear()
        self.v.clear()
        self.d.clear()
        self.graph()
        self.req.setText("")

class Programm:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = Window()
        self.window.show()
        sys.exit(self.app.exec_())


def Main():
    Programm()


# -- начало выполнения программы --
if __name__ == "__main__":
    Main()
