from django.shortcuts import render
from .models import *

# Create your views here.
def index(request):
    return render(request, "index.html")


def result(request):

    f1 = str(request.GET["f1"])
    f2 = str(request.GET["f2"])
    x0 = int(request.GET["x0"])
    nu = [float(request.GET["nu1"]), float(request.GET["nu2"])]
    a0 = int(request.GET["a0"])
    b0 = int(request.GET["b0"])
    a1 = int(request.GET["a1"])
    b1 = int(request.GET["b1"])
    A = int(request.GET["A"])
    B = int(request.GET["B"])
    a = int(request.GET["a"])
    b = int(request.GET["b"])
    e = float(request.GET["e"])
    q = float(request.GET["q"])
    p = float(request.GET["p"])
    k = int(request.GET["k"])
    
    d = Сondition(f1, f2, x0, nu, a0, b0, a1, b1, A, B, a, b, e, q, p, k)
    return render(request, 'result.html', {"data": d})
