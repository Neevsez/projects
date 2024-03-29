import pyfirmata as pf
import time as tm
import SpectrC14 as spec


class Programm:
    """Класс для консольного меню."""
    flag = True
    __mes = """
1 - Показать текущее положениеn\n
2 - Вернуть домой\n
3 - Ручное вращение\n
4 - Измерение\n
5 - фиксирование положения\n
6 - Закончить\n: 
"""

    def __init__(self, port, file) -> None:
        """Конструктор класса. При создании объекта класса указать порт и файл для выходных данных."""
        self.port = port
        self.file = file
        self.obj = spec.Unit(self.port, self.file)

    def __show(self) -> None:
        """Функция, вывода информации о положении установки"""
        print(self.obj)

    def __home(self) -> None:
        """Функция, возвращающая установку в начальное положение"""
        self.obj.Home()

    def __manual(self) -> None:
        """Функция, запускающая ручной режим"""
        self.obj.Manual_Start()

    def __automatic(self) -> None:
        """Фунция, автоматического управления"""
        self.obj.Start()

    def __fix(self) -> None:
        """Функция, фиксирующая начальное положение"""
        self.obj.Fix()

    def __menu(self):
        """Функция отобрадения меню"""
        while True:
            ans = input(self.__mes)
            if ans not in ["1", "2", "3", "4", "5", "6"]:
                continue
            else:
                break
        match int(ans):
            case 1:
                self.__show()
            case 2:
                self.__home()
            case 3:
                self.__manual()
            case 4:
                self.__automatic()
            case 5:
                self.__fix()
            case 6:
                self.flag = False

    def Start(self):
        while self.flag:
            self.__menu()

if __name__ == "__main__":
    port = "COM5"
    file = "SpectrC.dat"
    a = Programm(port, file)
    a.Start()
