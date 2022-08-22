from django.contrib import admin
from .models import Coleccion, Reto, Opciones_reto, Clave_usuario
from django.urls import path
from django.shortcuts import render
from .views import leer_documento_cargado, cargar_retos_bbdd
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

import os
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
        if request.method == 'POST' and 'archivocarga' in request.FILES:
            #print(request.POST['archivocarga'])
            doc = request.FILES
            #leer_documento_cargado(request.POST['archivocarga'])
            #leer_documento_cargado(request.FILES['archivocarga'])
            leer_documento_cargado(doc['archivocarga'])
            if cargar_retos_bbdd():
                if os.path.exists("archivos/carga.txt"):
                    os.remove("archivos/carga.txt")
                self.message_user(request, "El archivo CSV ha sido importado")
                return HttpResponseRedirect(".")
            else:
                return HttpResponse('no ok')
        return render(request, "admin/csv_upload.html")

admin.site.register(Coleccion, ColeccionAdmin) 
