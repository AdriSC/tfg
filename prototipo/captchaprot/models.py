from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Reto(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    texto = models.CharField(max_length=300)
    #topic = models.CharField(max_length=15)
    cuenta_respuestas = models.BigIntegerField(default=0)
    eleccion = models.CharField(max_length=20, default='null')
    umbral_eleccion = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    fiabilidad_opcion = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    def __str__(self):
        return self.texto
    
    def comprueba(self, opcion):
        return self.eleccion == 'null' or opcion == self.eleccion
                      
    def actualiza_eleccion(self):
        opciones = Opciones_reto.objects.filter(reto = self.id)
        setattr(self, 'cuenta_respuestas', self.cuenta_respuestas + 1)
        
        for op in opciones:
            fiabilidad = (op.cuenta/self.cuenta_respuestas)*100
            if fiabilidad > self.umbral_eleccion and fiabilidad > self.fiabilidad_opcion:
                setattr(self, 'eleccion', op.opcion)
                setattr(self,'fiabilidad_opcion', fiabilidad)
        
        self.save()
        
class Opciones_reto(models.Model):
    reto = models.ForeignKey(Reto, on_delete=models.CASCADE)
    opcion = models.CharField(max_length=20)
    cuenta = models.BigIntegerField(default=0)
    
    class Meta:
        unique_together = ['reto', 'opcion']

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
