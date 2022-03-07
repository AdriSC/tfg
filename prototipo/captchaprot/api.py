from django.http import HttpResponse
import json
from .models import Question, Answer


#var myObj = JSON.parse('{"preguntas":[{"id":123,"q":"What??????"}, {"id":124,"q":"Why??????"}, {"id":125,"q":"Where??????"}]}');

def reto(request):
    
    query = Question.objects.all()
    question_dict = {}
    question_list = []
    for q in query:
        aux = {}
        aux['id'] = q.id
        aux['q'] = q.text
        question_list.append(aux)

    question_dict['preguntas'] = question_list
    print(question_dict)
    json_res = json.dumps(question_dict)
    return HttpResponse(json_res)

