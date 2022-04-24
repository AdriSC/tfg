from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Clave_usuario
from .forms import Form_registro, Form_login
from random import randint
import string

#def index(request):
    
def registro(request):
    if request.method == 'POST':
        
        form = Form_registro(request.POST)
    else:
        form = Form_registro()

    return render(request, 'registro.html', {'form': form})

def crear_cuenta(request):
    usuario = User.objects.create_user(request.POST['nombre_usuario'], request.POST['email'], request.POST['contrasena'])
    
    cl = ''
    for i in range(32):
        rand_num = randint(0, len(string.ascii_letters) - 1)
        cl += string.ascii_letters[rand_num] 
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

    
  