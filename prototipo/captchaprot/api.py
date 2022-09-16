from random import randint
from django.http import HttpResponse
import json
from .models import Coleccion, Textos, Opciones_texto
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

def filtrar_colecciones(lista_ppcc, lista_pprr, lista_colecciones):
    colecciones_posibles = []
    colecciones_a_evitar = []
    lista_ids_validos =[]

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

    if len(lista_colecciones) > 0:
        return True
    else:
        return False

def selecciona_textos(textos_etiquetados, textos_sin_etiquetar, num_textos, lista_textos):
    
    num_et = num_textos//2 + 1
    num_sin_et = num_textos - num_et
    cont_textos = 0

    while cont_textos < num_et:
        rand_num = randint(0, len(textos_etiquetados) - 1)
        if textos_etiquetados[rand_num] != 'null':
            aux_dict = {}
            option_list = []
            challenge = textos_etiquetados[rand_num]
            textos_etiquetados[rand_num] = 'null'
            aux_dict['id'] = challenge.id
            aux_dict['text'] = challenge.texto
            
            opciones_query = Opciones_texto.objects.filter(texto=challenge)
            for o in opciones_query:
                    option_list.append(o.opcion)
            
            aux_dict['options'] = option_list
            lista_textos.append(aux_dict)
            cont_textos +=1
    
    cont_textos = 0
    while cont_textos < num_sin_et:
        rand_num = randint(0, len(textos_sin_etiquetar) - 1)
        if textos_sin_etiquetar[rand_num] != 'null':
            aux_dict = {}
            option_list = []
                
            challenge = textos_sin_etiquetar[rand_num]
            textos_sin_etiquetar[rand_num] = 'null'
            aux_dict['id'] = challenge.id
            aux_dict['text'] = challenge.texto
            opciones_query = Opciones_texto.objects.filter(texto=challenge)
            for o in opciones_query:
                    option_list.append(o.opcion)
            
            aux_dict['options'] = option_list
            lista_textos.append(aux_dict)
            cont_textos +=1

@csrf_exempt
def reto(request):

    requisitos = json.loads(request.body.decode())
    print(requisitos)
    ppcc = requisitos['palabras_clave'].split(',')
    if requisitos['palabras_restringidas'] != '':
        pprr = requisitos['palabras_restringidas'].split(',')
    else:
        pprr = []
  
    colecciones = []

    if filtrar_colecciones(ppcc, pprr, colecciones):
        criterio = Q(eleccion = 'null')
        textos_etiquetados = []
        textos_sin_etiquetar = []
        
        for c in colecciones:
            textos_etiquetados_qs= Textos.objects.filter(coleccion = c).filter(~criterio)
            textos_sin_etiquetar_qs = Textos.objects.filter(coleccion = c).filter(criterio)
            for r_et in textos_etiquetados_qs:
                textos_etiquetados.append(r_et)
            for r_sin in textos_sin_etiquetar_qs:
                textos_sin_etiquetar.append(r_sin)

        num_textos = requisitos['num_textos']
        lista_textos = []
        selecciona_textos(textos_etiquetados, textos_sin_etiquetar, num_textos, lista_textos)
        json_res = json.dumps({'reto':lista_textos})
        
    else:
        json_res = json.dumps({'reto':'no se han encontrado textos'})
    
    return HttpResponse(json_res)


@csrf_exempt
def comprobacion(request):
    resultados = json.loads(request.body.decode())
    respuestas = resultados['respuestas']
    comp_respuestas = [0,0]
    for resp in respuestas:
        texto_qs = Textos.objects.get(id = resp['id'])
        if texto_qs.eleccion != 'null':
           if texto_qs.comprueba(resp['respuesta']):
            comp_respuestas[0] +=1
        else:
            comp_respuestas[1] +=1
    
    if comp_respuestas[0] > comp_respuestas [1]:
        valoracion = 'correcto'
        for resp in respuestas:
            textos_query = Textos.objects.get(id = resp['id'])
            opcion_query = Opciones_texto.objects.get(texto = resp['id'], opcion = resp['a'])
            opcion_query.actualiza_cuenta()
            textos_query.actualiza_eleccion()
    else:
        valoracion = 'incorrecto'

    json_res = json.dumps({'resultado':valoracion})
    return HttpResponse(json_res)