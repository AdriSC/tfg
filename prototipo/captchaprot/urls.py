from django.urls import path

from . import views, api

urlpatterns = [
    path('', views.index, name='index'),
    path('reto', api.reto, name='reto'),
]