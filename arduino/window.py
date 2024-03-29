from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from Form import *
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import cv2
import numpy as np
import SpectrC14 as spec
from time import sleep


class ThreadOpenCV(Qt.QThread):
    changePixmap = Qt.pyqtSignal(Qt.QImage)

    def __init__(self):
        super().__init__()

    def run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FPS, 24)

        while True:
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_expanded = np.expand_dims(frame_rgb, axis=0)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                convertToQtFormat = Qt.QImage(
                    rgbImage.data, w, h, ch * w, Qt.QImage.Format_RGB888)
                p = convertToQtFormat.scaled(751, 600, Qt.Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

                if cv2.waitKey(1) == ord('q'):
                    break
            cv2.destroyAllWindows()


class Window(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self, dangl):
        super().__init__()
        self.setupUi(self)
        self.dangl = dangl
        self.set_progress_bar.setMinimum(0)
        self.set_progress_bar.setMaximum(100)
        self.set_progress_bar.setValue(0)

        self.set_values.clicked.connect(
            self.set_data)  # кнопка вводимых данных
        # очистка графика перед новым измерением
        self.clear_graph.clicked.connect(self.clear)
        self.simulation.clicked.connect(self.camera)

        # -- камера --
        self.thread = ThreadOpenCV()
        self.thread.changePixmap.connect(self.setImage)

        # -- график --
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.figure = Figure()
        self.axes = self.figure.gca()
        self.axes.set_title("plot")

    # -- функция записи вводимых данных --
    def __data(self):
        self.d = [
            float(self.ax_input.text()),
            float(self.ay_input.text()),
            float(self.df_input.text()),
            float(self.dfp_input.text()),
            (float(self.initial_angle_input.text()) / self.dangl),
            (float(self.end_angle_input.text()) / self.dangl),
        ]
        print(self.d)

    # def set_data(self):

    def clear(self):
        self.message()
        self.graph()

    # -- функция камеры --
    def camera(self):
        self.thread.start()

    def setImage(self, image):
        self.label_video.setPixmap(Qt.QPixmap.fromImage(image))

    # -- функция построения графика --
    def graph(self):
        self.axes.clear()
        self.axes.plot(self.k, self.v)

        self.axes.legend(["spectr"])
        self.axes.grid(True)

        self.canvas = FigureCanvas(self.figure)
        self.proxy_widget = self.scene.addWidget(self.canvas)

# -- диалоговое окно --
    def message(self):
        t = QtWidgets.QMessageBox()
        t.setWindowTitle("save")
        t.setText("Сохранить результат?")
        t.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        t.setIcon(QtWidgets.QMessageBox.Information)
        t.buttonClicked.connect(self.check_cliked)
        t.exec_()

# -- сохранение данных --
    def check_cliked(self, btn):
        if btn.text() == "Cancel":
            self.k.clear()
            self.v.clear()
            self.set_progress_bar.setValue(0)
        else:
            print("Ok")


# -- основные действия программы --
class Programm:
    def __init__(self, dangl):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = Window(dangl)
        self.window.show()
        sys.exit(self.app.exec_())


# -- программа --
def Main():
    port = "COM5"
    file = "SpectrC.dat"
    obj = spec.Unit(port, file)
    obj.Start()
    # dangl = 0.0006592
    # Programm(dangl)


# -- начало выполнения программы --
if __name__ == "__main__":
    Main()
