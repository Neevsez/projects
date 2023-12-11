from django.shortcuts import render
from .models import Newton
import sympy as sp

# Create your views here.
def index(request):
    return render(request, "index.html")

def test(request):
    t = sp.Symbol("x")
    f = sp.cos(t) - t ** 3
    a = Newton(f, 0.5, 0.01).Start()
    return render(request, 'index.html', {"func" : a})