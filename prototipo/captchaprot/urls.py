from django.urls import path

from . import views, api

urlpatterns = [
    path('reto', api.reto, name='reto'),
    path('comprobacion', api.comprobacion, name='comprobacion'),
    path('registro', views.registro, name='registro'),
    path('crear_cuenta', views.crear_cuenta, name='crear cuenta'),
    path('acceso', views.acceso, name='acceso'),
    path('iniciar_sesion', views.iniciar_sesion, name='iniciar sesion'),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('ventana_usuario', views.ventana_usuario, name='ventana_usuario')
]