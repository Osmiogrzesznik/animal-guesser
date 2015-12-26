# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import random
from adivinaconf import *

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)
 


def trad_sino(s):
    if len(s)==0:
        return None
    while s.lower() not in ACEPTABLE_SINO:
        s = raw_input('> ')
    if s in POS_SI:
        return SI
    if s in POS_NO:
        return NO

def si_es_no(s):
    if s ==SI:
        return NO
    return SI

def aprender(cosa):
    for preg,resp in respuestas_actual.iteritems():
            db[preg][resp]=set(db[preg][resp])
            db[preg][resp].add(cosa)
def obt_resp(preg):
    n = 0
    for resp in respuestas:
        if resp in db[preg][SI]:
        # if resp in db[preg][SI] or resp in db[preg][NO]:
            n+=1
    return n
def masgrande(st):
   t = zip([len(db[x][SI])+len(db[x][NO]) for x in st],[x for x in st])
   print t
   return max(t)[1]

def masgrande2(st):
    t = zip([obt_resp(x)for x in st],[x for x in st])
    return max(t)[1]    
def loaddb():
    fh = open('database_{}.json'.format(COSA),'r')
    rs = fh.read()
    db = json.loads(str(rs))
    return db

def savedb():
    global db
    fw = open('database_{}.json'.format(COSA),'w')
    fw.write(json.dumps(db,indent=0,cls=SetEncoder))
    fw.close()    

def generarsets():
    preguntas = set(db.iterkeys())
    respuestas = set()
    for resp in db.values():
        for t in resp.values():
            for cosa in t:
                respuestas.add(cosa)
    puntos = dict()
    for r in respuestas:
        puntos[r]=1

    return preguntas,respuestas,puntos
def maxpuntos():
    if len(puntos)<1: return (0,0)
    return max(zip(puntos.values(),puntos.keys()))

def main():
    print 'Vamos a jugar un juego, piensa en un {}, cuando quieras, aprieta enter.\n Cuando no sepa la respuesta, presione enter para saltar la pregunta'.format(COSA)
    raw_input('')
    global db
    global respuestas_actual
    global respuestas
    global puntos

    win = False
    db = loaddb()
    preguntas,respuestas,puntos = generarsets()
    respuestas_actual = dict()
    intentos = MAXINTENTOS

    while True:
        #Mientras queden respuestas y preguntas, y si estamos jugando con puntos, no haya un animal
        #que supere el puntaje máximo, hace una pregunta según su criterio (RANDOM, NUEVA_AI o tradicional)
        while len(respuestas)>0 and len(preguntas)>0 and (not PUNTOS or maxpuntos()[0]<PUNTAJEMAX):
            if RANDOM:
                p_actual = random.choice(list(preguntas))
            elif NUEVA_AI:
                p_actual = masgrande2(preguntas)
            else:
                p_actual = masgrande(preguntas)
            preguntas.remove(p_actual)
            print '¿Tu {} {}? (s/n)  '.format(COSA,p_actual),
            ra=trad_sino(raw_input(''))
            if ra is None:
                continue
            respuestas_actual[p_actual]=ra
            for e in respuestas.copy():     
                # Elimina el animal de los posibles si la respuesta no es la correcta, Y si está
                # activado el modo rápido Ó si sabe que la respuesta es la contraria
                if e not in db[p_actual][ra] and (RAPIDO or e in db[p_actual][si_es_no(ra)]):
                    respuestas.remove(e)
                    puntos.pop(e,None)
                elif e in db[p_actual][ra]:
                    puntos[e] = puntos.get(e,0) + 1
              
        #Si quedan respuestas posibles, y algún animal tiene 1 punto menos que el puntaje máximo, intenta achuntarle
        while (len(respuestas)>0 and (not PUNTOS or maxpuntos()[0] == PUNTAJEMAX)) or len(respuestas) in [1,2]:
            if PUNTOS:
                actual = maxpuntos()[1]
            else:
                actual= random.choice(list(respuestas))
            print '¿Tu {} es {}? (s/n) '.format(COSA,actual),
            ra= trad_sino(raw_input(''))
            if ra == SI:
                print 'Gané, jejeje'
                aprender(actual)
                win = True
                break
            if ra == NO:
                print 'No puede ser, nooooo!'
                intentos -=1
                puntos.pop(actual,None)
                if actual in respuestas: respuestas.remove(actual)

        if win: break
    
        #Si quedan respuestas, volver a intentar ()
        if intentos >0 and len(respuestas)>0 and len(preguntas)>0: continue
        
        #Si se acaban las respuestas, pregunta por nuevos animal y pregunta, y graba la información en la DB.
        else: 
            print 'Me rindo.¿Qué {} era?: '.format(COSA)
            nueva_cosa = raw_input(u'').lower()
            print "\nPerfecto.\nPodrías formular una pregunta de tipo 'sí o no' para diferenciar tu {}? (la respuesta debe ser sí)".format(COSA)
            print "Completa la siguiente oración: '¿Tu {} ...... ?'".format(COSA)
            while True:
                print "¿Tu {}...".format(COSA),
                pregunta_nueva = raw_input(u'').lower()
                if pregunta_nueva in preguntas or pregunta_nueva in respuestas_actual:
                    print 'Esa pregunta ya me la sé, intenta con otra.'
                    respuestas_actual[pregunta_nueva]=SI
                    continue
                elif len(pregunta_nueva)<1:
                    break
                respuestas_actual[pregunta_nueva]=SI
                db[pregunta_nueva]=dict()
                db[pregunta_nueva][SI] = set()
                db[pregunta_nueva][NO] = set()
                break
            aprender(nueva_cosa)
            print 'Querrías jugar de nuevo?   ',
            ra = trad_sino(raw_input(''))
            if ra == SI:
                savedb()
                preguntas,respuestas,puntos = generarsets()
                respuestas_actual = dict()
                intentos = MAXINTENTOS
                continue
            if ra == NO or ra is None:
                savedb()
                break
    
    

if __name__ == '__main__':
    main()
