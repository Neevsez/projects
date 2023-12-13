from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', index),
    path('result/', result, name="result"),
    path('admin/', admin.site.urls),
]