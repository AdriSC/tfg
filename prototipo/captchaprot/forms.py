import re
from django import forms 

class Form_registro(forms.Form):
    nombre_usuario = forms.CharField(label='Nombre de usuario', required=True)
    email = forms.CharField(label='Email', required=True)
    contrasena = forms.CharField(label='Contraseña', required=True)

class Form_login(forms.Form):
    nombre_usuario = forms.CharField(label='Nombre de usuario', required=True)
    contrasena = forms.CharField(label='Contraseña', required=True)