from random import randint
from django.http import HttpResponse
import json
from .models import Coleccion, Reto, Opciones_reto
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

def filtrar_colecciones(lista_ppcc, lista_pprr, lista_colecciones):
    colecciones_posibles = []
    colecciones_a_evitar = []
    lista_ids_validos =[]
    #colecciones_validas = []

    if len(lista_ppcc) > 0:
        for pc in lista_ppcc:
            query = Coleccion.objects.filter(palabras_clave__icontains=pc)
            for res in query:
                colecciones_posibles.append(res.id)
        colecciones_posibles = set(colecciones_posibles)
    
    if len(lista_pprr) > 0:
        for pr in lista_pprr:
            query = Coleccion.objects.filter(palabras_clave__icontains=pr)
            for res in query:
                colecciones_a_evitar.append(res.id)
        colecciones_a_evitar = set(colecciones_a_evitar)

    for posible in colecciones_posibles:
        if posible not in colecciones_a_evitar:
           lista_ids_validos.append(posible)
    
    for c_id in lista_ids_validos:
            c_aux = Coleccion.objects.get(id=c_id)
            lista_colecciones.append(c_aux)

    #print(colecciones_posibles)
    #print(colecciones_a_evitar)
    #print(lista_colecciones)
    if len(lista_colecciones) > 0:
        return True
    else:
        return False

def selecciona_retos(retos_etiquetados, retos_sin_etiquetar, num_retos, lista_retos):
    
    num_et = num_retos//2 + 1
    num_sin_et = num_retos - num_et
    cont_retos = 0
    #print([len(retos_etiquetados), len(retos_sin_etiquetar)])
    #print(retos_etiquetados)
    #print(retos_sin_etiquetar)

    while cont_retos < num_et:
        rand_num = randint(0, len(retos_etiquetados) - 1)
        if retos_etiquetados[rand_num] != 'null':
            aux_dict = {}
            option_list = []
            challenge = retos_etiquetados[rand_num]
            retos_etiquetados[rand_num] = 'null'
            aux_dict['id'] = challenge.id
            aux_dict['text'] = challenge.texto
            
            opciones_query = Opciones_reto.objects.filter(reto=challenge)
            for o in opciones_query:
                    option_list.append(o.opcion)
            
            aux_dict['options'] = option_list
            lista_retos.append(aux_dict)
            cont_retos +=1
    
    cont_retos = 0
    while cont_retos < num_sin_et:
        rand_num = randint(0, len(retos_sin_etiquetar) - 1)
        if retos_sin_etiquetar[rand_num] != 'null':
            aux_dict = {}
            option_list = []
                
            challenge = retos_sin_etiquetar[rand_num]
            retos_sin_etiquetar[rand_num] = 'null'
            aux_dict['id'] = challenge.id
            aux_dict['text'] = challenge.texto
            opciones_query = Opciones_reto.objects.filter(reto=challenge)
            for o in opciones_query:
                    option_list.append(o.opcion)
            
            aux_dict['options'] = option_list
            lista_retos.append(aux_dict)
            cont_retos +=1

@csrf_exempt
def reto(request):

    requisitos = json.loads(request.body.decode())
    #print(requisitos)
    ppcc = requisitos['palabras_clave'].split(',')
    if requisitos['palabras_restringidas'] != '':
        pprr = requisitos['palabras_restringidas'].split(',')
    else:
        pprr = []
        
    #print(ppcc)
    #print(pprr)
    #print(requisitos['num_retos'])
    
    colecciones = []

    if filtrar_colecciones(ppcc, pprr, colecciones):
        criterio = Q(eleccion = 'null')
        retos_etiquetados = []
        retos_sin_etiquetar = []
        
        for c in colecciones:
            retos_etiquetados_qs= Reto.objects.filter(coleccion = c).filter(~criterio)
            retos_sin_etiquetar_qs = Reto.objects.filter(coleccion = c).filter(criterio)
            for r_et in retos_etiquetados_qs:
                retos_etiquetados.append(r_et)
            for r_sin in retos_sin_etiquetar_qs:
                retos_sin_etiquetar.append(r_sin)

        num_retos = requisitos['num_retos']
        lista_retos = []
        selecciona_retos(retos_etiquetados, retos_sin_etiquetar, num_retos, lista_retos)
        json_res = json.dumps({'challenges':lista_retos})
        
    else:
        json_res = json.dumps({'challenges':'no se han encontrado retos'})
    
    #print(json_res)
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