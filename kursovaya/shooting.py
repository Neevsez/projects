class Euler:
    """Метод Эйлера для решения краевой задачи второго порядка в формате\n
    {y' = f1(x, y, z); z' = f2(x, y, z); alp0 * y + bet0 * y' = A; alp1 * y + bet1 * y' = B}\n
    Необходимые данные для реализации метода:\n
    f1(x, y, z) - функция в формате строки\n
    f2(x, y, z) - функция в формате строки\n
    x0 - начальная точка\n
    nu - значения y'(x0) (Для задачи Коши)\n
    alp0, bet0, apl1, bet1 - коэффициенты в краевых условиях\n
    A, B  - Правая часть краевых условий\n
    accuracy - Точность вычисления, указывается в количестве символов после запятой (accuracy = 3 | 0.001). 
    Если не указана, автоматически выставляется на 0.01.
    Внутри класс имеются методы:\n
    Calculation(q) - реализует метод Эйлера для решения Задачи Коши. Метод возвращает значение функций y и z в точке (b, B)\n
    func() - составляет и вычисляет значение функции для метода стрельбы. Метод возвращает значение функции
    """
    y = []
    z = []
    E = {
        "Type-Error": ["Выражение для функции должно быть записано в формате str", "Значение должно быть числом"],
        "Value-Error": ["Значение выражения записано неверно", "Введено неверное количество элементов. Необходимые элементы: f1, f2, x, nu, a0, b0, a1, b1, A, B"],
    }

    def __f(self, func, x, y, z) -> any:
        try:
            f = eval(func)
            return f
        except Exception as e:
            return e

    def __f3(self) -> any:
        y, z = self.Calculation()
        f = self.a1 * y + self.b1 * z - self.B
        return f

    def __str__(self) -> str:
        return f"y\' = {self.func1}\nz\' = {self.func2}\n{self.a0}y({self.a}) + {self.b0}y\'({self.a}) = {self.A}\n{self.a1}y({self.b}) + {self.b1}y\'({self.b}) = {self.B}"

    def __init__(self, *args, accuracy=2) -> None:
        try:
            if len(args) != 12:
                raise Exception(self.E["value-Error"][1])
            func1, func2, x, nu, a0, b0, a1, b1, A, B, a, b = args
            if (not isinstance(func1, str)) or (not isinstance(func2, str)):
                raise Exception(self.E["Type-Error"][0])
            if not isinstance(accuracy, int):
                raise Exception(self.E["Type-Error"][1])
            elif (accuracy < 0):
                raise Exception(self.E["value-Error"][0])
            if not isinstance(x, int) and not isinstance(x, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(a0, int) and not isinstance(a0, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(b0, int) and not isinstance(b0, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(a1, int) and not isinstance(a1, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(b1, int) and not isinstance(b1, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(A, int) and not isinstance(A, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(B, int) and not isinstance(B, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(a, int) and not isinstance(a, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(b, int) and not isinstance(b, float):
                raise Exception(self.E["Type-Error"][1])
            self.func1 = func1
            self.func2 = func2
            self.m = abs(b - a) * 10 ** accuracy
            self.h = 1 * (10 ** -accuracy)
            self.x = [x]
            if not isinstance(nu, int) and not isinstance(nu, float):
                raise Exception(self.E["Type-Error"][1])
            else:
                if b0 == 0:
                    self.y = [A / a0]
                    self.z = [nu]
                elif b0 != 0:
                    self.z = [(A - a0 * nu) / b0]
                    self.y = [nu]
            self.a0 = a0
            self.b0 = b0
            self.a1 = a1
            self.b1 = b1
            self.A = A
            self.B = B
            self.a = a
            self.b = b
            self.ac = accuracy
        except Exception as e:
            print(e)

    def Calculation(self, q=0) -> tuple:
        """В случае, если необходимо получить два массива со значениями функций y и z, 
        следует вписать переменную q, отличную от 0"""
        for i in range(1, self.m + 1):
            self.x.append(self.x[0] + self.h * i)
            self.y.append(self.y[i - 1] + self.h * self.__f(self.func1,
                          self.x[i - 1], self.y[i - 1], self.z[i - 1]))
            self.z.append(self.z[i - 1] + self.h * self.__f(self.func2,
                          self.x[i - 1], self.y[i - 1], self.z[i - 1]))
        if q == 0:
            return self.y[-1], self.z[-1]
        else:
            return self.y, self.z

    def func(self) -> any:
        return self.__f3()

    def get_x(self) -> list:
        return self.x


class Shooting:
    """Класс для реализации метода стрельбы\n
    nu - массив с двумя случайными значениями параметра\n
    {y' = f1(x, y, z); z' = f2(x, y, z); alp0 * y + bet0 * y' = A; alp1 * y + bet1 * y' = B}\n
    Необходимые данные для реализации метода:\n
    f1(x, y, z) - функция в формате строки\n
    f2(x, y, z) - функция в формате строки\n
    x0 - начальная точка\n
    alp0, bet0, apl1, bet1 - коэффициенты в краевых условиях\n
    A, B  - Правая часть краевых условий\n
    Внутри метода есть два доступных метода:\n
    Start() - метод, реализующий вычисление и параметра\n
    Requirement() - метод, возвращающий в формате строки полученную задачу Коши.
    """
    E = {
        "Type-Error": ["Выражение для функции должно быть записано в формате str", "Значение должно быть числом", "Значения параметров должны вводиться через массив"],
        "Value-Error": ["Значение выражения записано неверно", "Введено неверное количество элементов. Необходимые элементы: f1, f2, x, nu, a0, b0, a1, b1, A, B"],
        "Cycle-Error": ["Количество итераций превысило 100т"],
    }

    def __str__(self) -> str:
        return f"y\' = {self.f1}\nz\' = {self.f2}\n{self.a0}y({self.a}) + {self.b0}y\'({self.a}) = {self.A}\n{self.a1}y({self.b}) + {self.b1}y\'({self.b}) = {self.B}"

    def __init__(self, *args, accuracy=2) -> None:
        try:
            if len(args) != 12:
                raise Exception(self.E["Wrong value"][1])
            func1, func2, x, nu, a0, b0, a1, b1, A, B, a, b = args
            if (not isinstance(func1, str)) or (not isinstance(func2, str)):
                raise Exception(self.E["Type-Error"][0])
            if not isinstance(accuracy, int):
                raise Exception(self.E["Type-Error"][1])
            elif (accuracy < 0):
                raise Exception(self.E["Wrong value"][0])
            if not isinstance(x, int) and not isinstance(x, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(nu, list):
                raise Exception(self.E["Type-Error"][2])
            if not isinstance(a0, int) and not isinstance(a0, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(b0, int) and not isinstance(b0, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(a1, int) and not isinstance(a1, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(b1, int) and not isinstance(b1, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(A, int) and not isinstance(A, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(B, int) and not isinstance(B, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(a, int) and not isinstance(a, float):
                raise Exception(self.E["Type-Error"][1])
            if not isinstance(b, int) and not isinstance(b, float):
                raise Exception(self.E["Type-Error"][1])
            self.f1 = func1
            self.f2 = func2
            self.m = abs(b - a) * 10 ** accuracy
            self.h = 1 * (10 ** -accuracy)
            self.x0 = x
            self.nu = nu
            self.a0 = a0
            self.b0 = b0
            self.a1 = a1
            self.b1 = b1
            self.A = A
            self.B = B
            self.a = a
            self.b = b
            self.ac = accuracy
        except Exception as e:
            print(e)

    def __num(self, nu2, nu1) -> any:
        try:
            return nu2 - ((Euler(self.f1, self.f2, self.x0, nu2, self.a0, self.b0, self.a1, self.b1, self.A, self.B, self.a, self.b).func() * (nu2 - nu1)) / (Euler(self.f1, self.f2, self.x0, nu2, self.a0, self.b0, self.a1, self.b1, self.A, self.B, self.a, self.b).func() - Euler(self.f1, self.f2, self.x0, nu1, self.a0, self.b0, self.a1, self.b1, self.A, self.B, self.a, self.b).func()))
        except ZeroDivisionError:
            return nu2

    def Start(self) -> any:
        i = 1
        try:
            while True:
                if i == 100000:
                    raise Exception(self.e["Cycle-Error"][0])
                if (self.nu[i] == self.nu[i - 1]):
                    del self.nu[-1]
                    break
                o = self.__num(self.nu[i], self.nu[i - 1])
                self.nu.append(o)
                i += 1
            return self.nu[-1]
        except Exception as e:
            print(e)
            return self.nu[-1]

    def Data(self, q=1) -> tuple:
        o = self.Start()
        obj = Euler(self.f1, self.f2, self.x0, o, self.a0, self.b0,
                    self.a1, self.b1, self.A, self.B, self.a, self.b, accuracy=self.ac)
        x = obj.get_x()
        y, z = obj.Calculation(1)
        if q == 1:
            return x, y
        else:
            return y, z

    def Requirement(self) -> str:
        o = self.Start()
        f = f"y\' = z\nz\' = {self.f2}\ny({self.x0}) = {self.A}\nz({self.x0}) = {o}"
        return f


def Main() -> any:
    q = 0
    k = 1
    while q >= 0:
        f1 = "z"
        f2 = f"-1 + 0.49 * {q ** 2} - 0.98 * {q} * z"
        x0 = 0
        nu = [1, -1]
        a0 = 1
        b0 = 0
        a1 = 1
        b1 = 0
        A = 0
        B = 0
        a = 0
        b = 1
        obj = Shooting(f1, f2, x0, nu, a0, b0, a1, b1, A, B, a, b, accuracy=2)
        y, z = obj.Data(0)
        for i in range(0, len(z), 10):
            print(k - 1, i / 100, round(y[i], 10), round(z[i], 10), sep="\t")
        q = z[k]
        k += 1
        print("\n")


if __name__ == "__main__":
    Main()
