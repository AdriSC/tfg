from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Coleccion(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=300)
    palabras_clave = models.CharField(max_length=300)
    
    def __str__(self):
        return self.nombre
        
class Textos(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    texto = models.CharField(max_length=300)
    coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE)
    cuenta_respuestas = models.BigIntegerField(default=0)
    eleccion = models.CharField(max_length=20, default='null')
    umbral_eleccion = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    fiabilidad_opcion = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.texto
    
    def comprueba(self, opcion):
        return self.eleccion == 'null' or opcion == self.eleccion
                      
    def actualiza_eleccion(self):
        opciones = Opciones_texto.objects.filter(texto = self.id)
        setattr(self, 'cuenta_respuestas', self.cuenta_respuestas + 1)
        
        for op in opciones:
            fiabilidad = (op.cuenta/self.cuenta_respuestas)*100
            if fiabilidad > self.umbral_eleccion and fiabilidad > self.fiabilidad_opcion:
                setattr(self, 'eleccion', op.opcion)
                setattr(self,'fiabilidad_opcion', fiabilidad)
                
        self.save()
        
class Opciones_texto(models.Model):
    texto = models.ForeignKey(Textos, on_delete=models.CASCADE)
    opcion = models.CharField(max_length=20)
    cuenta = models.BigIntegerField(default=0)
    
    class Meta:
        unique_together = ['texto', 'opcion']

    def __str__(self):
        return self.opcion
    
    def actualiza_cuenta(self):
        setattr(self, 'cuenta', self.cuenta + 1)
        self.save()
    
class Clave_usuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    clave = models.CharField(max_length=32)

    def __str__(self):
        return self.clave

    def renueva_clave(self, nueva_clave):
        setattr(self, 'clave', nueva_clave)
        self.save()

    def comprueba_clave(self, clave_usuario): 
        return self.clave == clave_usuario
