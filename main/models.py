from django.db import models
import sympy as sp

# Create your models here.
class Shooting:
    def __str__(self) -> str:
        return f"y\' = {self.f1}\nz\' = {self.f2}\n{self.a0}y({self.a}) + {self.b0}y\'({self.a}) = {self.A}\n{self.a1}y({self.b}) + {self.b1}y\'({self.b}) = {self.B}"

    def __f(self, func, x, y, z) -> any:
        f = eval(func)
        return f

    def __f3(self, nu) -> any:
        y, z = self.__euler(nu)
        f = self.a1 * y[-1] + self.b1 * z[-1] - self.B
        return f

    def __num(self, nu2, nu1) -> any:
        try:
            return nu2 - ((self.mean(nu2) * (nu2 - nu1)) / (self.mean(nu2) - self.mean(nu1)))
        except ZeroDivisionError:
            return nu2

    def __start(self) -> any:
        i = 1
        while True:
            if (round(self.nu[i], 10) == round(self.nu[i - 1], 10)):
                del self.nu[-1]
                break
            o = self.__num(self.nu[i], self.nu[i - 1])
            self.nu.append(o)
            i += 1
        return self.nu[-1]

    def __euler(self, nu) -> tuple:
        self.x = [round(self.x0, 10)]
        if self.b0 == 0:
            self.y = [self.A / self.a0]
            self.z = [nu]
        elif self.b0 != 0:
            self.z = [(self.A - self.a0 * nu) / self.b0]
            self.y = [nu]
        for i in range(1, self.m + 1):
            self.x.append(round(self.x[0] + self.h * i, 10))
            self.y.append(round(self.y[i - 1] + self.h * self.__f(self.f1,
                          self.x[i - 1], self.y[i - 1], self.z[i - 1]), 10))
            self.z.append(round(self.z[i - 1] + self.h * self.__f(self.f2,
                          self.x[i - 1], self.y[i - 1], self.z[i - 1]), 10))
        return self.y, self.z

    def __init__(self, f1, f2, x0, nu, a0, b0, a1, b1, A, B, a, b, e=0.01) -> None:
        self.f1 = f1
        self.f2 = f2
        self.x0 = x0
        self.nu = nu
        self.a0 = a0
        self.b0 = b0
        self.a1 = a1
        self.b1 = b1
        self.A = A
        self.B = B
        self.a = a
        self.b = b
        self.e = e
        self.m = int(abs(b - a) / e)
        self.h = e

    def mean(self, nu) -> any:
        return self.__f3(nu)

    def Data(self) -> tuple:
        o = self.__start()
        y, z = self.__euler(o)
        return self.x, y, z


def test(f1, f2, x0, nu, a0, b0, a1, b1, A, B, a, b, e, q, p):
    Y = [[0 for i in range(int(1 / e) + 1)]]

    k = 1
    l = 1
    flag = True
    while flag:
        f2_n = sp.simplify(f2)
        f2_n = f2_n.subs("q", q)
        f2_n = str(f2_n)
        obj = Shooting(f1, f2_n, x0, nu, a0, b0, a1, b1, A, B, a, b, e)
        x, y, z = obj.Data()
        q = z[k]
        p = y[k]

        Y.append(y)
        for i in range(len(Y[l])):
            if i == len(Y[l]) - 1:
                flag = False
            if abs(Y[l][i] - Y[l - 1][i]) < e:
                continue
            else:
                break
        l += 1
        k += int(1 / (e * 10))
    d = {
        "x": x[::int(1 / (e * 10))],
        "y": y[::int(1 / (e * 10))],
        "z": z[::int(1 / (e * 10))],
    }
    return d


def Main() -> any:
    q = 0
    p = 0
    l = 1
    k = 1
    Y = [[0 for i in range(101)]]
    flag = True
    while flag:
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
        obj = Shooting(f1, f2, x0, nu, a0, b0, a1, b1, A, B, a, b, 0.01)
        x, y, z = obj.Data()
        q = z[k]
        p = y[k]
        Y.append(y)
        for i in range(len(Y[l])):
            if i == len(Y[l]) - 1:
                print(y[::10])
                flag = False
            if abs(Y[l][i] - Y[l - 1][i]) < 0.01:
                continue
            else:
                break
        ans = input(": ")
        if ans == "":
            l += 1
            k += 10
            continue
        else:
            break


if __name__ == "__main__":
    Main()
