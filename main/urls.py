from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', index),
    path('test/', test, name="test"),
    path('admin/', admin.site.urls),
]