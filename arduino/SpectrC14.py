import pyfirmata as pf
import time as tm
import keyboard as kb


class Unit:
    """
    В конструкторе класса есть два поля:
    port - обязательное поле, в которое необходимо указать порт, которому подключена плата.\n
    file - название файла, в который будут сохранятся результаты измерения. Поле является необязательным, 
    в случае если имя файла не указано, будет создан файл 'output.dat'.\n
    """
    delay = tm.sleep(0.005)
    n = 9  # количество поворотов призмы
    m = 16  # количество поворотов фотоприёмника
    dangl = 0.0006592
    fi = 0
    l = 0

    def __str__(self) -> str:
        """Перегрузка оператора вывода. Если плата подключена, будет выведено 'connected'"""
        return f"fi = {self.fi} l = {self.l} angle = {self.fi * self.dangl}"

    def __rotate(self, direction, manual=0, *steps) -> None:
        """Функция поворота. На вход подаётся только направление поворота(0, 1). Шаги задаются отдельно
        Пример: self.__rotate(0)\n
        manual - ручное управление. Если не требуется не указывать. \n
        steps - кортеж из двух значений, первое количество шагов поворота стола, второе - фотоприёмника"""
        if manual != 0:
            steps = list(steps)
            try:
                if len(steps) > 2:
                    raise Exception("Wrong lenght")
                n, m = steps[0], steps[-1]
            except Exception as e:
                print(e)
        else:
            n, m = self.n, self.m
        for i in range(n):
            self.p["p8"].write(direction)
            self.p["p7"].write(1)
            self.delay
            self.p["p7"].write(0)
            self.delay
        for j in range(m):
            self.p["p10"].write(direction)
            self.p["p9"].write(1)
            self.delay
            self.p["p9"].write(0)
            self.delay
        if (direction == 0):
            self.fi -= n
            self.l -= m
        elif (direction == 1):
            self.fi += n
            self.l += m
        else:
            self.fi = 0
            self.l = 0

    def __init__(self, port, file="output.dat") -> None:
        self.file = file  # название файла
        self.board = pf.Arduino(port)
        self.p = {
            "p1": self.board.get_pin('d:13:o'),
            "p2": self.board.get_pin('d:12:o'),
            "p3": self.board.get_pin('d:9:o'),
            "p4": self.board.get_pin('d:10:o'),
            "p7": self.board.get_pin('d:5:o'),
            "p8": self.board.get_pin('d:4:o'),
            "p9": self.board.get_pin('d:3:o'),
            "p10": self.board.get_pin('d:2:o'),
        }
        """верхний транслятор (12, 13)
            p1, p2 - y-трансляция стола
            нижний транслятор (9, 10)
            p3, p4 - x-трансляция стола
            p7, p8 - вращение стола
            p9, p10 - вращение фотоприемника"""
        self.a = {
            "a0": self.board.get_pin('a:4:i'),
            "a1": self.board.get_pin('a:2:i'),
            "a2": self.board.get_pin('d:11:i'),
            "a3": self.board.get_pin('d:8:i'),
            "a4": self.board.get_pin('a:5:i'),
            "a5": self.board.get_pin('a:3:i'),
        }
        """a0 - фотоприемник №1   'a:0:i' подвижный
            a1 - фотоприемник №2   'a:1:i' опорный
            a2, a3 - концевик №1 и №2
            a4 - фотоприемник №3
            a5 - фотоприемник №4"""

    def Start(self) -> None:
        """Основная функция для автоматической работы с платой. В начале функия запрашивает 2 значения: начальный угол и конечный угол.
        После введения углов, если начальный угол меньше(больше) 0, то установка подстаривается под необходимые параметры.
        Во время измерения все полученные значения записываются в файл."""
        self.it = pf.util.Iterator(self.board)
        self.it.start()
        fii = int(
            float(input("Введите начальное значение fi: ")) / self.dangl)
        fif = int(float(input("Введите конечное значение fi: ")) / self.dangl)
        fs = open(self.file, "w+", newline="")
        print(f"fii = {fii}, fif = {fif}")
        tm.sleep(0.2)
        if fii < 0:
            while self.fi > fii:
                self.__rotate(0)
        elif fii > 0:
            while self.fi < fii:
                self.__rotate(1)

        print(f"fi = {self.fi}, fii = {fii}, fif = {fif}")
        while self.fi <= fif:
            self.__rotate(1)
            fs.write(
                f"{self.fi * self.dangl} {self.a['a0'].read()}\n"
            )
            print(
                f"fi = {self.fi}, l = {self.l} angle = {self.fi * self.dangl} R = {self.a['a0'].read()}"
            )
        fs.close()

    def Home(self) -> None:
        """Функция возрвращающая призму и фотоприёмник в начальное положение."""
        print("go home")
        if self.fi > 0 and self.l > 0:
            self.__rotate(0, 1, self.fi, self.l)
            tm.sleep(1)
        elif self.fi < 0 and self.l < 0:
            self.__rotate(1, 1, abs(self.fi), abs(self.l))
            tm.sleep(1)
        elif self.fi < 0 and self.l > 0:
            self.__rotate(1, 1, abs(self.fi), 0)
            self.__rotate(0, 1, 0, self.l)
        elif self.fi > 0 and self.l < 0:
            self.__rotate(0, 1, self.fi, 0)
            self.__rotate(1, 1, 0, abs(self.l))
        elif self.fi > 0 and self.l == 0:
            self.__rotate(0, 1, self.fi, 0)
        elif self.fi < 0 and self.l == 0:
            self.__rotate(1, 1, abs(self.fi), 0)
        elif self.fi == 0 and self.l > 0:
            self.__rotate(0, 1, 0, self.l)
        elif self.fi == 0 and self.l < 0:
            self.__rotate(1, 1, 0, abs(self.l))
        elif self.fi == 0 and self.l == 0:
            print("In home")
        else:
            print("unknown")

    def Fix(self) -> None:
        """Функция фиксирующая начальное положение стола и фотоприёмника."""
        self.__rotate(2, 1, 0, 0)

    def Manual_Start(self) -> None:
        """Функция для ручного управления:\n
        1 - одношаговый поворот призмы назад\n
        alt + 1 - 500-шаговый поворот призмы назад\n
        2 - одношаговый поворот призмы вперёд\n
        alt + 2 - 500-шаговый поворот призмы вперёд\n
        3 - одношаговый поворот фотоприёмника назад\n
        alt + 3 - 500 - шаговый поворот фотоприёмника назад\n
        4 - одношаговый поворот фотоприёмника вперёд\n
        alt + 4 - 500 - шаговый поворот фотоприёмника\n
        с - выход из ручного режима (после выхода в консоль запишутся все введённые значения)
        """
        kb.add_hotkey("1", lambda: self.__rotate(0, 1, 1, 0))
        kb.add_hotkey("alt + 1", lambda: self.__rotate(0, 1, 500, 0))
        kb.add_hotkey("2", lambda: self.__rotate(1, 1, 1, 0))
        kb.add_hotkey("alt + 2", lambda: self.__rotate(1, 1, 500, 0))
        kb.add_hotkey("3", lambda: self.__rotate(0, 1, 0, 1))
        kb.add_hotkey("alt + 3", lambda: self.__rotate(0, 1, 0, 500))
        kb.add_hotkey("4", lambda: self.__rotate(1, 1, 0, 1))
        kb.add_hotkey("alt + 4", lambda: self.__rotate(1, 1, 0, 500))
        while True:
            kb.wait("c")
            break
        kb.unhook_all_hotkeys()


"""
Функция Main() - основная функция для запуска программы в этом файле. При запуске с другого файла проигнорировать
"""


def Main() -> None:
    """port - порт платы\n
    obj - объект класса управления установкой"""
    port = "COM5"
    obj = Unit(port, "SpectrC.dat")
    print(obj)


if __name__ == "__main__":
    Main()
