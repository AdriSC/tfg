from django.contrib import admin
from .models import Reto, Opciones_reto, Clave_usuario

# Register your models here.

admin.site.register(Reto) 
admin.site.register(Opciones_reto)
admin.site.register(Clave_usuario)
