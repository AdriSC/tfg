from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.conf import settings
from django.http import HttpResponse, Http404

from .models import Clave_usuario, Coleccion, Opciones_reto, Reto
from .forms import Form_registro, Form_login
from random import randint

from django.views.decorators.csrf import csrf_exempt

import string
import csv
import os

def generar_clave():
    clave = ''
    for i in range(32):
        rand_num = randint(0, len(string.ascii_letters) - 1)
        clave += string.ascii_letters[rand_num]
    return clave

#def index(request):
    
def registro(request):
    if request.method == 'POST':
        
        form = Form_registro(request.POST)
    else:
        form = Form_registro()

    return render(request, 'registro.html', {'form': form})

def crear_cuenta(request):
    usuario = User.objects.create_user(request.POST['nombre_usuario'], request.POST['email'], request.POST['contrasena'])
    
    cl = generar_clave()
    clave = Clave_usuario(usuario=usuario, clave=cl)
    clave.save()

    return HttpResponseRedirect('acceso')

def acceso(request):
    if request.method == 'POST':
        
        form = Form_login(request.POST)
    else:
        form = Form_login()

    return render(request, 'login.html', {'form': form})

def iniciar_sesion(request):

    user=authenticate(username=request.POST['nombre_usuario'], password=request.POST['contrasena'])
    if user is not None:
        login(request, user)
        
        return HttpResponseRedirect('ventana_usuario')
    else:
        return HttpResponse('no existe usuario')

def cerrar_sesion(request):
    logout(request)
    return HttpResponseRedirect('acceso')

def ventana_usuario(request):

    if '_auth_user_id' in request.session:
        clave_usuario = Clave_usuario.objects.get(usuario=request.session['_auth_user_id'])
        return HttpResponse("Tu clave de usuario: " + clave_usuario.clave)
    else:
        return HttpResponseRedirect('acceso')

def renovar_clave(request):
    clave = Clave_usuario.objects.get(usuario=request.session['_auth_user_id'])
    print(clave.clave)
    clave.renueva_clave(generar_clave())
    return HttpResponseRedirect('ventana_usuario')

def leer_documento_cargado(archivo):
    with open('archivos/carga.txt', mode='wb+') as carga_doc:
        for c in archivo.chunks():
            carga_doc.write(c)

def comprobar_datos(fila, opciones):
    if len(fila) != 3 or len(opciones) < 2:
        return False
    else:
        return True

def cargar_retos_bbdd():
    with open('archivos/carga.txt') as doc_carga:
        doc_rd = csv.reader(doc_carga)
        cabecera = next(doc_rd)
        ppcc = next(doc_rd)
        c = Coleccion(nombre=cabecera[0], descripcion=cabecera[1], palabras_clave=ppcc[0])
        c.save()
        for fila in doc_rd:
            print(fila)
            opciones = fila[1].strip('[]').split(';')
            if comprobar_datos(fila, opciones):
                try:
                    r = Reto(texto=fila[0], coleccion=c, umbral_eleccion = float(fila[2]))
                    r.save()
                except ValueError:
                    return False
                
                for op in opciones:
                    o = Opciones_reto(reto=r, opcion=op)
                    o.save()
            else: 
                return False
    return True

@csrf_exempt
def subir_retos(request):
    if request.method == 'POST':
        print(request.FILES)
        leer_documento_cargado(request.FILES['archivocarga'])
        if cargar_retos_bbdd():
            if os.path.exists("archivos/carga.txt"):
                os.remove("archivos/carga.txt")
            return HttpResponse('ok')
        else:
            return HttpResponse('no ok')




def descargar_csv(request):

    csv_res = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="datos_etiquetados.csv"'},
    )

    cabecera = ['Texto', 'Opción elegida', 'Aceptacion']

    textos = Reto.objects.raw('SELECT id, texto, eleccion, fiabilidad_opcion FROM captchaprot_reto')

    filas = []
   
    for t in textos:
        fila = []
        fila.append(t.texto)
        fila.append(t.eleccion)
        fila.append(t.fiabilidad_opcion)
        filas.append(fila)
    
    doc_wr = csv.writer(csv_res)
    doc_wr.writerow(cabecera)
    doc_wr.writerows(filas)

    return csv_res

    
    

