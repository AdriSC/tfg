from random import randint
from django.http import HttpResponse
import json
from .models import Reto, Opciones_reto
from django.views.decorators.csrf import csrf_exempt

def reto(request):
    
    retos_query = Reto.objects.raw('SELECT id, texto FROM captchaprot_reto')
    
    result_list = []

    for r in retos_query:
        result_list.append(r)

    challenges_list = []
    num_retos = 0
    while num_retos != 3:
        rand_num = randint(0, len(result_list) - 1)
        if result_list[rand_num] != 'null':
            aux_dict = {}
            option_list = []
            
            challenge = result_list[rand_num]
            result_list[rand_num] = 'null'
            aux_dict['id'] = challenge.id
            aux_dict['text'] = challenge.texto
            
            opciones_query = Opciones_reto.objects.raw('SELECT id, opcion FROM captchaprot_opciones_reto WHERE reto_id = %s', [challenge.id])
            for o in opciones_query:
                option_list.append(o.opcion)
        
            aux_dict['options'] = option_list
            challenges_list.append(aux_dict)
            num_retos += 1
    
    json_res = json.dumps({'challenges':challenges_list})
    return HttpResponse(json_res)


@csrf_exempt
def comprobacion(request):
    
    resultados = json.loads(request.body.decode())
    respuestas = resultados['respuestas']
    suma = 0
    aciertos = [0,0]
    comprobaciones = {}
    for respuesta in respuestas:
        r = json.loads(respuesta)
        reto_query = Reto.objects.get(id = r['id'])
        opcion_query = Opciones_reto.objects.get(reto = r['id'], opcion = r['a'])
        opcion_query.actualiza_cuenta()
        reto_query.actualiza_eleccion()

        if reto_query.comprueba(r['a']):
            aciertos[0] +=1
        else:
            aciertos[1] +=1

    
    if aciertos[0] > aciertos [1]:
        p = 'ok'
    else:
        p = 'ko'

    json_res = json.dumps({'resultado':p})
    return HttpResponse(json_res)
