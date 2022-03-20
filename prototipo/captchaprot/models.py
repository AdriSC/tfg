from django.db import models

# Create your models here.

class Challenges(models.Model):
    #id = models.IntegerField(primary_key=True)
    id = models.BigAutoField(primary_key=True, auto_created=True)
    text = models.CharField(max_length=300)
    #topic = models.CharField(max_length=15)
    option1 = models.CharField(max_length=15)
    rate1 = models.BigIntegerField(default=0)
    option2 = models.CharField(max_length=15)
    rate2 = models.BigIntegerField(default=0)
    option3 = models.CharField(max_length=15)
    rate3 = models.BigIntegerField(default=0)
    choice = models.CharField(max_length=15, default='ND')
    choiceRatio = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    # lista de opciones
    # lista de respuestas
    # umbral fiabilidad
    # fiabilidad opcion

    def __str__(self):
        return self.text  

    def calculaRatio(self):
        total = self.rate1 + self.rate2 + self.rate3
        opcion = ''
        ratio = 0
        
        if self.rate1 > self.rate2 and self.rate1 > self.rate3:
            ratio = (self.rate1/total) * 100
            opcion = self.option1
        elif self.rate2 > self.rate1 and self.rate2 > self.rate3:
            ratio = (self.rate2/total) * 100
            opcion = self.option2
        elif self.rate3 > self.rate1 and self.rate3 > self.rate2:
            ratio = (self.rate3/total) * 100
            opcion = self.option3

        if ratio >= 80:
            setattr(self, 'choice', opcion)
            setattr(self, 'choiceRatio', ratio)
            self.save()

    def compruebaYActualiza(self, op):
        resultado = False
        
        if self.choice == 'ND' or op == self.choice:
            resultado = True

        if op == self.option1:
            setattr(self, 'rate1', self.rate1 + 1)
        elif request.POST['opcion'] == q.option2:
            setattr(self, 'rate2', self.rate2 + 1)
        elif request.POST['opcion'] == q.option3:
            setattr(self, 'rate3', self.rate3 + 1)

        self.save()

        return resultado