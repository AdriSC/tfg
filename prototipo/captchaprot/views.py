from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, Http404

from .models import Clave_usuario, Coleccion, Opciones_reto, Reto
from .forms import Form_registro, Form_login
from random import randint

from django.views.decorators.csrf import csrf_exempt

import string
import csv
import os
import json

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
        return render(request, 'menu_usuario.html', {'clave': clave_usuario.clave, 'username': request.user.username})
        #return HttpResponse("Tu clave de usuario: " + clave_usuario.clave)
    else:
        return HttpResponseRedirect('acceso')

def renovar_clave(request):
    clave = Clave_usuario.objects.get(usuario=request.session['_auth_user_id'])
    print(clave.clave)
    clave.renueva_clave(generar_clave())
    return HttpResponseRedirect('ventana_usuario')

def leer_documento_cargado(archivo):
    with open('archivos/carga.txt', mode='wb+') as carga_doc:
        #for c in archivo.chunks():
        for c in archivo:
            carga_doc.write(c)
        print(carga_doc)
   

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

def ver_colecciones(request):
    colecciones_qs = Coleccion.objects.all()
    lista_cols = []
    for col_r in colecciones_qs:
        col_dict = {
            'id_coleccion': col_r.id,
            'nombre': col_r.nombre,
            'descripcion': col_r.descripcion,
            'palabras_clave': col_r.palabras_clave
        }
        lista_cols.append(col_dict)
    
    json_res = json.dumps({'colecciones':lista_cols})
    return HttpResponse(json_res)

def ver_retos_coleccion(request):
    id_col = request.GET['id_coleccion']
    criterio = Q(eleccion = 'null')

    retos_etiquetados_qs= Reto.objects.filter(coleccion = id_col).filter(~criterio).order_by('-cuenta_respuestas')
    retos_sin_etiquetar_qs = Reto.objects.filter(coleccion = id_col).filter(criterio)

    lista_r_et = []
    for r_et in retos_etiquetados_qs:
        r_dict = {
            'texto': r_et.texto,
            'eleccion': r_et.eleccion,
            'fiabilidad': str(r_et.fiabilidad_opcion)
        }
        lista_r_et.append(r_dict)

    lista_r_sin_et = []
    for r_sin_et in retos_sin_etiquetar_qs:
        r_dict = {
            'texto': r_sin_et.texto,
            'eleccion': r_sin_et.eleccion,
            'fiabilidad': str(r_sin_et.fiabilidad_opcion)
        }
        lista_r_sin_et.append(r_dict)
    
    json_res = json.dumps({
        'retos_etiquetados': lista_r_et,
        'retos_sin_etiquetar': lista_r_sin_et
    })    

    return HttpResponse(json_res)


@csrf_exempt
def subir_retos(request):
    if request.method == 'POST' and 'archivocarga' in request.FILES:
        print(request.FILES)
        #print(request.POST['archivocarga'])
        doc = request.FILES
        print(doc)
        #leer_documento_cargado(request.POST['archivocarga'])
        #leer_documento_cargado(request.FILES['archivocarga'])
        leer_documento_cargado(doc['archivocarga'])
        if cargar_retos_bbdd():
            if os.path.exists("archivos/carga.txt"):
                os.remove("archivos/carga.txt")
            return HttpResponse('ok')
        else:
            return HttpResponse('no ok')

def descargar_csv(request):

    id_col = request.GET['id_coleccion']
    coleccion_qs = Coleccion.objects.get(id = id_col)
    textos_qs= Reto.objects.filter(coleccion = id_col)

    cabecera = ['Texto', 'Opción elegida', 'Aceptacion']
    
    info_coleccion = [coleccion_qs.nombre, coleccion_qs.descripcion]
    filas = []
   
    for t in textos_qs:
        fila = []
        fila.append(t.texto)
        fila.append(t.eleccion)
        fila.append(t.fiabilidad_opcion)
        filas.append(fila)
    
    csv_res = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="{}.csv"'.format(coleccion_qs.nombre)},
    )

    doc_wr = csv.writer(csv_res)
    doc_wr.writerow(info_coleccion)
    doc_wr.writerow(cabecera)
    doc_wr.writerows(filas)

    return csv_res
    

