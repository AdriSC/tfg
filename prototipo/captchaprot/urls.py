from django.urls import path
from django.conf.urls.static import static


from . import views, api, admin

urlpatterns = [
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
    path('ver_retos_coleccion', views.ver_retos_coleccion, name='ver_retos_coleccion'),
    path('subir_retos', views.subir_retos, name='subir_retos'),
    path('descargar_csv', views.descargar_csv, name='descargar_csv'),
    path('upload-csv', admin.ColeccionAdmin.upload_csv, name="upload-csv"),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)