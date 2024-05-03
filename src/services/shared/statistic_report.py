#respuestas - arreglo con el valor de cada respuesta que se selecciono en el formulario
#mejores_respuestas - arreglo con el valor de la mejor respuesta de cada pregunta del formualario
#ponderacion_por_respuesta - arreglo el indice de valor de cada respuesta (Alta, Media, baja)
import numpy as np


def analyze(responses, response_weights):
    score = np.dot(responses, response_weights)

    return score


#lista_de_respuestas - lista de listas con cada una de las respuestas de un formulario
#lista_ponderacion_de_respuestas - lista con el valor ponderado de cada respuesta recibida del formulario
#estadistico_final_de_las_respuestas - media de los valores dentro de lista_ponderacion_de_respuestas
#diferencia_entre_respuesta_ideal_estadistico_final - diferencia entre la respuesta ideal del formulario y la media de las respuestas recibidas
#Conclusion_del_riesgo - conclusion entre si es riesgo alto medio o casi nulo
def conclusion_del_riesgo(responses, best_responses, response_weights):
    response_scores = []
    best_response = analyze(best_responses, response_weights)

    for response in responses:
        response_scores.append(analyze(response, response_weights))

    response_mean = np.mean(response_scores)

    risk = ((best_response - estadistico_final_de_las_respuestas) * 100) / best_response

    if risk >= 60:
        return 'Riesgo Alto'
    elif risk >= 30 and risk <= 60:
        return 'Riesgo Medio'
    else: 
        return 'Riesgo Bajo'


    
