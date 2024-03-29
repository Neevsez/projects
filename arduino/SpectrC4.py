import csv
import pyfirmata as pf
from time import sleep


class Board:
    def __init__(self, port, dangl):
        self.a = pf.Arduino(port)
        print("Подключение")
        self.board = pf.util.Iterator(self.a)
        self.board.start()
        print("Ардуина подключилась")

        self.dangl = dangl
        self.tb = 0.0005

        self.p1 = self.a.get_pin('d:13:o')  # верхний транслятор (12, 13)
        self.p2 = self.a.get_pin('d:12:o')  # p1, p2 - y-трансляция стола
        self.p3 = self.a.get_pin('d:9:o')  # нижний транслятор (9, 10)
        self.p4 = self.a.get_pin('d:10:o')  # p1, p2 - y-трансляция стола
        self.a2 = self.a.get_pin('d:11:i')  # концевик №1 и 2
        self.a3 = self.a.get_pin('d:8:i')  # концевик №3 и 4

        self.p7 = self.a.get_pin('d:5:o')
        self.p8 = self.a.get_pin('d:4:o')  # p7, p8 - вращение стола
        self.p9 = self.a.get_pin('d:3:o')
        self.p10 = self.a.get_pin('d:2:o')  # p9, p10 - вращение фотоприемника

        self.a4 = self.a.get_pin('a:5:i')  # фотоприемник №3
        # фотоприемник №1   'a:0:i' подвижный
        self.a0 = self.a.get_pin('a:4:i')
        self.a5 = self.a.get_pin('a:3:i')  # фотоприемник №4
        self.a1 = self.a.get_pin('a:2:i')  # фотоприемник №2   'a:1:i' опорный

    def start(self, ax, ay, fii, fif):
        print("Измерение")
        k = []
        v = []
        fi = 0
        n3 = 0
        n4 = 0
        sx = 0
        sy = 0
        print('ax= ', ax, 'ay= ', ay)
    #    sleep(10)

        if ax > 0:
            while sx < ax:   # смещение стола на (ax>0) шагов по оси x
                self.p1.write(1)
                self.p2.write(1)
                sleep(self.tb)
                self.p2.write(0)
                sleep(self.tb)
                sx = sx + 1
        if ax < 0:
            while sx > ax:   # смещение стола на (ax<0) шагов по оси x
                self.p1.write(0)
                self.p2.write(0)
                sleep(self.tb)
                self.p2.write(1)
                sleep(self.tb)
                sx = sx - 1.
        sx = 0

        if ay > 0:
            while sy < ay:  # смещение стола на (ay>0) шагов по оси y 78
                self.p4.write(1)
                self.p3.write(1)
                sleep(self.tb)
                self.p3.write(0)
                sleep(self.tb)
                sy = sy + 1.
        if ay < 0:
            while sy > ay:  # смещение стола на (ay<0) шагов по оси y
                self.p4.write(0)
                self.p3.write(0)
                sleep(self.tb)
                self.p3.write(1)
                sleep(self.tb)
                sy = sy - 1.
        sy = 0

        print('fii= ', fii, 'fif= ', fif)
        sleep(0.2)

    # НАЧАЛО
        with open('SpectrС.dat', 'w', newline='') as f:
            w = csv.writer(f)
            if fii < 0.:     # поворот призмы на угол FII
                while fi >= fii:
                    # экспериментальное вращение
                    self.p8.write(0)
                    sleep(self.tb)
                    self.p7.write(1)
                    sleep(self.tb)
                    self.p7.write(0)
                    fi = fi - 1
                f1i = 0
                while f1i >= fii * 2:
                    self.p10.write(0)
                    self.p9.write(1)
                    sleep(self.tb)
                    self.p9.write(0)
                    sleep(self.tb)
                    f1i = f1i - 1

            if fii > 0.:
                while fi < fii:
                    self.p8.write(1)
                    sleep(self.tb)
                    self.p7.write(1)
                    sleep(self.tb)
                    self.p7.write(0)
                    fi = fi + 1
                f1i = 0
                while f1i < fii * 2:
                    self.p10.write(1)
                    self.p9.write(1)
                    sleep(self.tb)
                    self.p9.write(0)
                    sleep(self.tb)
                    f1i = f1i + 1
            n4 = 0

            while fi <= fif:  # вращение призмы в диапазоне (FII, FIF)
                self.p8.write(1)
                self.p7.write(1)
                sleep(self.tb)
                self.p7.write(0)
                sleep(self.tb)
                fi = fi + 1
                while n3 < 2:  # вращение фотоприемника и запись данных с него
                    self.p10.write(1)
                    an0 = self.a0.read()
                    an1 = self.a1.read()
                    sleep(self.tb)
                    row = (fi*self.dangl, an0, an1)
                    w.writerow(row)
                    print('fi=', fi, fi * self.dangl, 'R=', an0)
                    k.append(fi * self.dangl)
                    v.append(an0)
                    self.p9.write(1)
                    sleep(self.tb)
                    self.p9.write(0)
                    n3 = n3 + 1
                    n4 = n4 + 1
                n4 = fi * 2
                n3 = 0
            return k, v, fi, n4

    def home(self, fi, n4):
        print('Go home')
        while fi > 0:   # возврат призмы в "исходное" положение
            self.p8.write(0)
            self.p7.write(1)
            sleep(self.tb)
            self.p7.write(0)
            sleep(self.tb)
            self.p10.write(0)
            fi = fi - 1.

        while n4 > 0:
            self.p10.write(0)
            self.p9.write(1)
            sleep(self.tb)
            self.p9.write(0)
            sleep(self.tb)
            n4 = n4 - 1
        print("set")

