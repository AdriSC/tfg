from django.urls import path
from django.conf.urls.static import static


from . import views, api, admin

urlpatterns = [
    path('', views.index, name='index'),
    path('reto', api.reto, name='reto'),
    path('comprobacion', api.comprobacion, name='comprobacion'),
    path('registro', views.registro, name='registro'),
    path('crear_cuenta', views.crear_cuenta, name='crear cuenta'),
    path('acceso', views.acceso, name='acceso'),
    path('iniciar_sesion', views.iniciar_sesion, name='iniciar sesion'),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('ventana_usuario', views.ventana_usuario, name='ventana_usuario'),
    path('renovar_clave', views.renovar_clave, name='renovar_clave'),
    path('ver_colecciones', views.ver_colecciones, name='ver_colecciones'),
    path('ver_colecciones', views.ver_colecciones, name='ver_colecciones'),
    path('ver_textos_coleccion', views.ver_textos_coleccion, name='ver_textos_coleccion'),
    path('subir_textos', views.subir_textos, name='subir_textos'),
    path('descargar_csv', views.descargar_csv, name='descargar_csv'),
    path('upload-csv', admin.ColeccionAdmin.upload_csv, name="upload-csv"),
]