from django.db import models

# Create your models here.

class Question(models.Model):
    #id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=300)
    # lista de opciones
    # lista de respuestas
    # umbral fiabilidad
    # fiabilidad opcion

      
    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, primary_key=True, on_delete=models.CASCADE)
    solution = models.CharField(max_length=10)
    # frecuencia opcion

    def __str__(self):
        return self.solution

    

    