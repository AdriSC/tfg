from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Question, Answer

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    template = loader.get_template('reto.html')
    context = {}
    return HttpResponse(template.render(context, request))

  