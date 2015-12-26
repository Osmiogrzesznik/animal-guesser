# -*- coding: utf-8 -*-
SI = "si"
NO = "no"
POS_SI= ['si','s','sí','yes','y']
POS_NO= ['no','n']
ACEPTABLE_SINO = POS_SI + POS_NO
COSA = "animal" #"persona", "cosa", "película"
RANDOM = False
NUEVA_AI = True
RAPIDO = False
PUNTOS = True
PUNTAJEMAX = 5
MAXINTENTOS = 6

'''Este es el archivo de configuración del juego de adivinanza de animales
SI: palabra a usar para representar "sí"
NO: palabra a usar para representar "no"
POS_SI y POS_NO: palabras utilizables como respuesta

COSA: cosa a adivinar, el juego originalmente es de animales, pero puede usarse
para cualquier objeto o persona. Para poder cambiar el juego, es necesario empezar
manualmente una nueva base de datos con el nombre "database_COSA.json" y el formato
#                                                 #
#       {PREGUNTA:{SI:[RESPUESTA],NO:[]}}         #
#                                                 #
donde SI y NO corresponden a las variables especificadas en este archivo, y PREGUNTA y RESPUESTA
corresponde a una pregunta y respuesta iniciales, entre comillas.

RANDOM: desactiva la "inteligencia artificial" y hace preguntas aleatoriamente
#                                       #
#    valores posibles: True o False     #
#                                       #

RAPIDO: activa inteligencia artificial de descarte rápido de animales.
Si no sabe la respuesta a un determinado animal, lo descarta. Aprende menos,
pero hace el juego más rápido.
#                                       #
#    valores posibles: True o False     #
#                                       #

NUEVA_AI: Nueva inteligencia artificial de selección de preguntas, según el número 
de respuestas disponibles, a diferencia de la anterior, que lo hace con todas las 
respuestas. No funciona si se usa en conjunto con RANDOM. Si se usa en conjunto con
RAPIDO puede hacer el juego demasiado rápido.
#                                       #
#    valores posibles: True o False     #
#                                       #

PUNTOS: Habilita el sistema de puntos, que hace que el programa intente adivinar un animal alcanzado
determinado número de puntos (respuestas adecuadas para cada animal).
#                                       #
#    valores posibles: True o False     #
#                                       #

PUNTAJEMAX: Número de puntos necesarios para que el programa intente adivinar.

MAXINTENTOS: Número máximo de intentos que el programa hace antes de rendirse.

'''
