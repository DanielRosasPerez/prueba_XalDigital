import json
import requests
from datetime import datetime
from pprint import pprint

def pregunta_1(json_response: json) -> None:
    """
    Está función imprime la respuesta a la pregunta 1, la cual nos dice :
    Obtener el número de respuestas contestadas y no contestadas.
    """
    preguntas_contestadas = 0
    numero_total_de_respuestas = 0
    preguntas_sin_respuestas = 0
    for dct in json_response["items"]:
        if dct["is_answered"]:
            preguntas_contestadas += 1
            numero_total_de_respuestas += dct["answer_count"]
        else:
            preguntas_sin_respuestas += 1
    print("Preguntas contestadas : ", preguntas_contestadas)
    print("Número total de respuestas : ", numero_total_de_respuestas)
    print("Preguntas sin respuestas : ", preguntas_sin_respuestas)

def pregunta_2(json_response: json) -> None:
    """
    Está función imprime la respuesta a la pregunta 2, la cual nos dice :
    Obtener la respuesta con menor número de vistas.
    """
    conteo_vistas_y_titulos = [(dct["view_count"], dct["title"]) for dct in json_response["items"]]
    conteo_vistas_y_titulos.sort(key=lambda x: x[0])
    conteo_vista, titulo_pregunta = conteo_vistas_y_titulos[0]
    print("Pregunta con menor número de vistas : ", titulo_pregunta)
    print("Número de vistas : ", conteo_vista)

def pregunta_3(json_response: json) -> None:
    """
    Está función imprime la respuesta a la pregunta 3, la cual nos dice :
    Obtener la respuesta más vieja y más actual.
    """
    fechas_creacion_y_titulos = [(datetime.fromtimestamp(dct["creation_date"]), dct["title"]) 
                                    for dct in json_response["items"]]
    fechas_creacion_y_titulos.sort(key=lambda x: x[0])
    _, pregunta_vieja = fechas_creacion_y_titulos[0]
    _, pregunta_reciente = fechas_creacion_y_titulos[-1]
    print("Pregunta más vieja : ", pregunta_vieja)
    print("Pregunta más reciente : ", pregunta_reciente)

def pregunta_4(json_response: json) -> None:
    """
    Está función imprime la respuesta a la pregunta 4, la cual nos dice :
    Obtener la respuesta del owner que tenga una mayor reputación.
    """
    reputaciones_y_titulos = [(dct["owner"]["reputation"], dct["title"]) for dct in json_response["items"] 
                                if "reputation" in dct["owner"]]
    reputaciones_y_titulos.sort(key=lambda x: x[0])
    reputacion, titulo = reputaciones_y_titulos[-1]
    print("Pregunta del owner con mayor reputación : ", titulo)
    print("Reputación : ", reputacion)

def funcion_principal(json_response: json, preguntas: dict) -> None:
    """
    Está función nos va a permitir imprimir de forma ordenada en consola,
    las funciones que arrojan la respuesta a las preguntas del test técnico,
    en la parte de programación.
    """
    for indice, key in enumerate(preguntas,start=1):
        print('~'*80)
        print(f"Pregunta {indice} : {key}")
        print("Respuesta : ")
        print()
        funcion_a_ejecutar = preguntas[key]
        funcion_a_ejecutar(json_response)

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/\
                            88.0.4324.96 Chrome/88.0.4324.96 Safari/537.36"}

api_link = "https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle=perl&site=stackoverflow"

response = requests.get(url=api_link,headers=headers, timeout=15)
if response.status_code == 200:
    json_response = response.json()
    preguntas = {
                    "Obtener el número de respuestas contestadas y no contestadas": pregunta_1,
                    "Obtener la respuesta con menor número de vistas": pregunta_2,
                    "Obtener la respuesta más vieja y más actual": pregunta_3,
                    "Obtener la respuesta del owner que tenga una mayor reputación": pregunta_4
                }
    funcion_principal(json_response, preguntas)
