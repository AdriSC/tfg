from django.contrib import admin
from .models import Coleccion, Reto, Opciones_reto, Clave_usuario
from django.urls import path
from django.shortcuts import render
#from views import subir_retos
from django.http import HttpResponse, HttpResponseRedirect

# Register your models here.

#admin.site.register(Coleccion) 
admin.site.register(Reto) 
admin.site.register(Opciones_reto)
admin.site.register(Clave_usuario)


class ColeccionAdmin(admin.ModelAdmin):
    change_list_template = "coleccion/coleccion_change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):
        return render(request, "admin/csv_upload.html")

admin.site.register(Coleccion, ColeccionAdmin) 
