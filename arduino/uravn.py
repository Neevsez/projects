import sympy as sp
import math as m


def newton(y, y_pr, x):
    i = 0
    while True:
        y0 = y.subs(t, x[i])
        ypr0 = y_pr.subs(t, x[i])
        q = round(x[i] - (y0 / ypr0), 5)
        x.append(q)
        i += 1
        if abs(x[i] - x[i - 1]) < 0.0001:
            break
    return x


t = sp.Symbol("x")
y = sp.cos(3 * t) - 1 + m.sqrt(3) * sp.sin(t)
y_pr = sp.diff(y)

f = []
x = []
l = []
m = []
n0 = 2
n = n0 * sp.pi
while n <= 2 * n0 * sp.pi:
    q = y_pr.subs(t, n)
    if round(q, 1) == 0:
        f.append(n)
    n += 0.01

for j in range(len(f)):
    z1 = [f[j] - 0.15]
    z2 = [f[j] + 0.15]
    x.append(z1)
    x.append(z2)

for j in range(len(x)):
    q = newton(y, y_pr, x[j])
    l.append(q[-1])

l.sort()
for item in l:
    if item not in m and item <= 2 * n0 * sp.pi - 1:
        m.append(item)

print(m)