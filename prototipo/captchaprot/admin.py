from django.contrib import admin
from .models import Coleccion, Reto, Opciones_reto, Clave_usuario

# Register your models here.

admin.site.register(Coleccion) 
admin.site.register(Reto) 
admin.site.register(Opciones_reto)
admin.site.register(Clave_usuario)
