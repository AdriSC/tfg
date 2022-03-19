from datetime import datetime
from random import randint
from urllib.request import Request
from django.http import HttpResponse
import json
from .models import Challenges

#var myObj = JSON.parse('{"preguntas":[{"id":123,"q":"What??????"}, {"id":124,"q":"Why??????"}, {"id":125,"q":"Where??????"}]}');

def reto(request):
    
    #qText = 'SELECT id, text, option1, option2, option3 FROM captchaprot_challengues'
    query = Challenges.objects.raw('SELECT id, text, option1, option2, option3 FROM captchaprot_challenges')
    
    result_list = []

    for q in query:
        result_list.append(q)

    question_dict = {}
    challenges_list = []
    numRetos = 0
    while numRetos != 3:
        randNum = randint(0, len(result_list) - 1)
        print("size " + str(len(result_list)))
        print("random " + str(randNum))
        if result_list[randNum] != 'null':
            aux_dict = {}
            option_list = []
            
            
            challenge = result_list[randNum]
            result_list[randNum] = 'null'
            aux_dict['id'] = challenge.id
            aux_dict['text'] = challenge.text
            option_list.append(challenge.option1)
            option_list.append(challenge.option2)
            option_list.append(challenge.option3)
            aux_dict['options'] = option_list
            challenges_list.append(aux_dict)
            numRetos += 1
    
    #res_dict = {}
    #res_dict['challengues'] = challenges_list
    json_res = json.dumps({'challenges':challenges_list})
    return HttpResponse(json_res)


#{'opciones':[{'id':, 'opcion':},{'id':, 'opcion':},{'id':, 'opcion':},]}

def comprobacion(request):
    q = Challenges.objects.get(id = request.POST['id'])
    
    resultado = 'ko'
    if q.choice == 'ND' or request.POST['opcion'] == q.choice:
        resultado = 'ok'

    if request.POST['opcion'] == q.option1:
        q.update(rate1 = q.rate1 + 1)
    elif request.POST['opcion'] == q.option2:
        q.update(rate2 = q.rate2 + 1)
    elif request.POST['opcion'] == q.option3:
        q.update(rate3 = q.rate3 + 1)

    q.calculaRatio()
    dict_res = {}
    dict_res['id'] = request.POST['id']
    dict_res['resultado'] = resultado
    json_res = json.dumps(dict_res)
    
    return HttpResponse(json_res)
