# -*- coding: utf-8 -*-
import gettext
import json
import random
from adivinaconf import *
en = gettext.translation('guesser', localedir='locale', languages=['en'])
en.install()

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

class GuessGame():
    def __init__(self):
        self.win = False
        self.db = self.loaddb()
        self.questions,self.answers,self.points = self.generate_sets()
        self.current_answers = dict() #Dictionary that holds question:answer value pairs for current THING
        self.tries = MAXTRIES      
        
        
    def ask(self):
        #translate an input to a standard YES or NO answer.
        s = input('')
        if len(s)==0:
            return None
        while s.lower() not in ACCEPTABLE_YESNO:
            s = input('> ')
        if s in POS_YES:
            return YES
        if s in POS_NO:
            return NO

    def yes_to_no(self,s):
        if s ==YES:
            return NO
        return YES

    def learn_new(self,thing):
        for quest,answ in self.current_answers.items():
                self.db[quest][answ]=set(self.db[quest][answ])
                self.db[quest][answ].add(thing)

    def largest(self,st):
        #find questions with more "answers" on database, given a set of possible questions
        t = list(zip([len(self.db[x][YES])+len(self.db[x][NO]) for x in st],[x for x in st]))
        return max(t)[1]

    def largest2(self,st):
        #find the question with more "YES answers" on current remaining answers set
        t = list(zip([self.get_answer_n(x)for x in st],[x for x in st]))
        return max(t)[1]

    def get_answer_n(self,quest):
        #given a question, returns the number of remaining possible answers that have a positive (YES) answer
        n = 0
        for answ in self.answers:
            if answ in self.db[quest][YES]:
                n+=1
        return n   

    def loaddb(self):
        fh = open('database_{}.json'.format(THING),'r')
        rs = fh.read()
        db = json.loads(str(rs))
        return db

    def savedb(self):
        fw = open('database_{}.json'.format(THING),'w')
        fw.write(json.dumps(self.db,indent=0,cls=SetEncoder))
        fw.close()    

    def generate_sets(self):
        #generate separate sets for questions, possible answers, and dictionary for points.
        questions = set(self.db.keys())
        answers = set()
        for answ in list(self.db.values()):
            for t in list(answ.values()):
                for thing in t:
                    answers.add(thing)
        points = dict()
        for r in answers:
            points[r]=1
        return questions,answers,points

    def maxpoints(self):
        #get the current THING with most points
        if len(self.points)<1: return (0,0)
        return max(list(zip(list(self.points.values()),list(self.points.keys()))))

    def nextquestion(self):
        if RANDOM:
            c_question = random.choice(list(self.questions))
        elif NEW_AI:
            c_question = self.largest2(self.questions)
        else:
            c_question = self.largest(self.questions)
        return c_question

    def guess(self):
        if POINTS:
            actual = self.maxpoints()[1]
        else:
            actual= random.choice(list(self.answers))
        print(_('¿Tu %s es %s? (s/n) ') % (THING,actual)) 
        ca= self.ask()
        if ca == YES:
            print(_('Gané, jejeje'))
            self.learn_new(actual)
            self.win = True
        if ca == NO:
            print(_('No puede ser, nooooo!'))
            self.tries -=1
            self.points.pop(actual,None)
            if actual in self.answers: self.answers.remove(actual)
        

    def play(self):
        while True:
            #As long as there are possible answers and questions, and, if we are playing with points, no THING has more
            #than MAXPOINTS, choose a question from the set using one of three methods: RANDOM, NEW_AI or default.
            while len(self.answers)>0 and len(self.questions)>0 and (not POINTS or self.maxpoints()[0]<MAXPOINTS):
                c_question = self.nextquestion()
                self.questions.remove(c_question)
                print(_('¿Tu %s %s? (s/n)  ') % (THING,c_question), end=' ')
                ca=self.ask()
                if ca is None:
                    continue
                self.current_answers[c_question]=ca
                for e in self.answers.copy():     
                    #Removes the THING from possible answers set if wrong answer. If FAST is set to True, remove 
                    #even if no info is avaliable. Otherwise, remove it only if in 
                    if e not in self.db[c_question][ca] and (FAST or e in self.db[c_question][self.yes_to_no(ca)]):
                        self.answers.remove(e)
                        self.points.pop(e,None)
                    elif e in self.db[c_question][ca]:
                        self.points[e] = self.points.get(e,0) + 1
                  
            #If there are possible answers, and some THING has the maximum points, tries to guess. Also, if only two or one 
            #answers remain, guess anyway.
            while not self.win and self.tries>0 and ((len(self.answers)>0 and (not POINTS or self.maxpoints()[0] == MAXPOINTS)) or len(self.answers) in [1,2]):
                self.guess()
            
            if self.win: break
            #If there are tries left, and there are possible answers, try again
            if self.tries >0 and len(self.answers)>0 and len(self.questions)>0: continue
            
            #If there are no answers left, surrender. Ask for name of the new_thing, and suitable question.
            else: 
                print(_('Me rindo.¿Qué %s era?: ') % (THING))
                new_thing = input('').lower()
                print(_("\nPerfecto.\nPodrías formular una pregunta de tipo 'sí o no' para diferenciar tu %s? (la respuesta debe ser sí)") % (THING))
                print(_("Completa la YESguiente oración: '¿Tu %s ...... ?'") % (THING))
                while True:
                    print(_("¿Tu %s...") % (THING), end=' ')
                    new_question = input('').lower()
                    if new_question in self.questions or new_question in self.current_answers:
                        #If question already on db, ask for new question (but save answer anyway)
                        print(_('Esa pregunta ya me la sé, intenta con otra.'))
                        self.current_answers[new_question]=YES
                        continue
                    elif len(new_question)<1:
                        break
                    self.current_answers[new_question]=YES
                    self.db[new_question]=dict()
                    self.db[new_question][YES] = set()
                    self.db[new_question][NO] = set()
                    break
                self.learn_new(new_thing)  
                self.savedb()
                break  
        
if __name__ == '__main__':
    print(_('Vamos a jugar un juego, piensa en un %s, cuando quieras, aprieta enter.\n Cuando no sepa la respuesta, preYESone enter para saltar la pregunta') % (THING))
    input('')
    while True:
        game = GuessGame()
        game.play()
        print(_('Querrías jugar de nuevo?   '))
        ca = game.ask()
        if ca == YES:
            continue
        if ca == NO or ca is None:
            break