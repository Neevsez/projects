from PyQt5 import QtWidgets, QtCore, QtGui, Qt
from new_form import *
import sys
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import cv2
import numpy as np
from SpectrC4 import *
from time import sleep
import time
import cam_test as test


class ThreadOpenCV(Qt.QThread):
    changePixmap = Qt.pyqtSignal(Qt.QImage)

    def __init__(self):
        super().__init__()
        self.flag = True

    def run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FPS, 24)
        detector = test.handDetector(detectionCon=0.75, maxHands=2)
        totalFingers = 0

        while True:
            if self.flag == False:
                break
            else:
                sucess, img = cap.read()
                if sucess:
                    img = cv2.flip(img, 1)
                    img = detector.findHands(img)
                    lmList, bbox = detector.findPosition(img, draw=False)
                    if lmList:
                        fingersUp = detector.fingersUp()
                        totalFingers = fingersUp.count(1)
                    frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    frame_expanded = np.expand_dims(frame_rgb, axis=0)
                    rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgbImage.shape
                    convertToQtFormat = Qt.QImage(
                        rgbImage.data, w, h, ch * w, Qt.QImage.Format_RGB888)
                    p = convertToQtFormat.scaled(
                        751, 600, Qt.Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)

            # cv2.rectangle(img, (0, 0), (100, 100), (255, 255, 255), cv2.FILLED)
            # cv2.putText(img, str(totalFingers), (20, 75), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 13)

            cv2.destroyAllWindows()


class Window(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self, board, port, dangl):
        super().__init__()
        self.setupUi(self)
        self.board = board
        self.port = port
        self.dangl = dangl
        self.V = []
        self.K = []

        self.set_progress_bar.setMinimum(0)
        self.set_progress_bar.setMaximum(100)
        self.set_progress_bar.setValue(0)

        self.set_values.clicked.connect(
            self.set_data)  # кнопка вводимых данных
        # очистка графика перед новым измерением
        self.clear_graph.clicked.connect(self.clear)
        self.simulation.clicked.connect(self.camera)
        self.destroy_camera.clicked.connect(self.destroy_cam)

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

    def set_data(self):
        tic = time.perf_counter()

        self.__data()
        self.set_progress_bar.setValue(0)
        self.k, self.v, fi, n4 = self.board.start(
            self.d[0], self.d[1], self.d[4], self.d[5])
        self.set_progress_bar.setValue(50)
        sleep(5)
        self.board.home(fi, n4)
        self.set_progress_bar.setValue(100)
        self.graph()

        toc = time.perf_counter()
        print("\n")
        print(f"Заняло {toc - tic:0.4f} секунд")
        print("\n")

    def clear(self):
        self.message()
        self.graph()

    # -- функция камеры --
    def camera(self):
        self.thread.flag = True
        self.thread.start()

    def destroy_cam(self):
        self.thread.flag = False

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
        t.setStandardButtons(QtWidgets.QMessageBox.Ok |
                             QtWidgets.QMessageBox.Cancel)
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
            a = self.k.copy()
            b = self.v.copy()
            self.K.append(a)
            self.V.append(b)
            self.k.clear()
            self.v.clear()
            self.set_progress_bar.setValue(0)


# -- основные действия программы --
class Programm:
    def __init__(self, port, dangl):
        self.a = Board(port, dangl)

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = Window(self.a, port, dangl)
        self.window.show()
        sys.exit(self.app.exec_())


# -- программа --
def Main():
    port = "COM5"
    dangl = 0.0006592
    Programm(port, dangl)


# -- начало выполнения программы --
if __name__ == "__main__":
    Main()
