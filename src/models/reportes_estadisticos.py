#respuestas - arreglo con el valor de cada respuesta que se selecciono en el formulario
#mejores_respuestas - arreglo con el valor de la mejor respuesta de cada pregunta del formualario
#ponderacion_por_respuesta - arreglo el indice de valor de cada respuesta (Alta, Media, baja)

import numpy as np 
def analisis_por_respuesta(respuestas,ponderacion_por_respuesta):

    ponderacion_final_de_la_respuesta = np.dot(respuestas,ponderacion_por_respuesta)
    return ponderacion_final_de_la_respuesta
    
def analisis_de_la_mejor_respuesta(mejores_respuestas, ponderacion_por_respuesta):

    ponderacion_final_de_la_respuesta = np.dot(mejores_respuestas,ponderacion_por_respuesta)

    return ponderacion_final_de_la_respuesta

#lista_de_respuestas - lista de listas con cada una de las respuestas de un formulario
#lista_ponderacion_de_respuestas - lista con el valor ponderado de cada respuesta recibida del formulario
#estadistico_final_de_las_respuestas - media de los valores dentro de lista_ponderacion_de_respuestas
#diferencia_entre_respuesta_ideal_estadistico_final - diferencia entre la respuesta ideal del formulario y la media de las respuestas recibidas
#Conclusion_del_riesgo - conclusion entre si es riesgo alto medio o casi nulo
def conclusion_del_riesgo(lista_de_respuestas, mejor_respuesta, ponderacion_por_respuesta):

    lista_ponderacion_de_respuestas = []
    best_response = analisis_de_la_mejor_respuesta(mejor_respuesta)

    for  i in lista_de_respuestas:
        lista_ponderacion_de_respuestas.append(analisis_por_respuesta(i,ponderacion_por_respuesta))

    estadistico_final_de_las_respuestas = np.mean(lista_ponderacion_de_respuestas)

    diferencia_entre_respuesta_ideal_estadistico_final = best_response - estadistico_final_de_las_respuestas

    conclusion = (diferencia_entre_respuesta_ideal_estadistico_final*100) / best_response

    if conclusion >= 60:
        return 'Riesgo Alto'
    elif conclusion >= 30 and conclusion <= 60:
        return 'Riesgo Medio'
    else: 
        return 'Riesgo Bajo'


    
