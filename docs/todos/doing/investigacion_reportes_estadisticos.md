# Investigación: reportes estadísticos

## Responsable: Juan José

* ¿Qué operaciones se llevarán a cabo con los números provistos de los cuestionarios?
    - Cada pregunta en cada una de sus opciones de respuesta debe de contar con una ponderación, las ponderaciones desde mi punto de vista las puede
    llegar a poner el usuario a como el guste, también podemos nosotros meter mano y hacer que los usuarios deban de repartir un 100% entre todas sus
    opciones, esto nos obligaría a crear alguna clase de validación.
    - si hacemos esto de repartir el 100% a cada una de las opciones yo agarraría cada ponderación de las respuestas y las diviría entre 100 para no 
    tener une estadístico de numeros muy grandes.
    - una vez ya cuente con todas las respuestas realizaré una sumatoria y la compararé con la sumatoria ideal del cuestionario.
    - para saber que tan ideal sería cada pregunta sacaría la media obtenida de las sumatorias obtenidas de cada una de las respuestas de los usuarios
    después le restaría a la sumatoria ideal esta media y con eso nos queda la diferencia entre la sumatoria ideal y la media de las respuestas obtenidas
    , una vez tenemos esa diferencia podemos hacer una regla de tres para saber el porcentaje de "riesgo" que se obtuvo por parte de los cuestionarios,

                                                    100% --- sumatoria ideal
                                                    %%  --- diferencia media de las respuestas
    
    dependiendo de que tan alto sea el porcentaje de riesgo lo podemos clasificar en una categoría de 60% - 100% = riesgo alto, 30% - 60% riesgo medio, 0% - 30% = bajo riesgo


* ¿Qué números necesitamos de los cuestionarios?
    - Es fundamental que al momento que el usuario este creando un cuestionario, me comparta cuál de las opciones es por así decirlo la idea (o sea la
    de mayor valor) para yo poder obtener la sumatoria ideal directamente.
    - también se me ocurre que podríamos ponerle una opción a cada pregunta del cuestionario que sería como (priority) podemos poner simplemente Alta, media, regular 
    si es Alta multiplicariamos la ponderación de esa respuesta por 3, si es media por 2 y si es regular la dejaríamos sin multiplicador.

* ¿Qué estructuras de datos utilizaremos?
    - un diccionario en donde venga la ponderación de la pregunta ideal mapeada con su priority
    - un array numérico con todas las respuestas que introdujo el usuario.

DETALES: TODO