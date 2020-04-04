# -*- coding: utf-8 -*-
YES = "yes"  # "si"
NO = "no"  # "no"
POS_YES = ['tak',
           'ta',
           'oczywiście',
           'si',
           's',
           'sí',
           'yes',
           'y',
           "ani chybi",
           "bez dwóch zdań",
           "bezspornie",
           "bezsprzecznie",
           "jak najbardziej",
           "jakże by inaczej",
           "jasne",
           "ma się rozumieć",
           "na bank",
           "na mur",
           "naturalnie",
           "nie inaczej",
           "nie ma dwóch zdań",
           "oczywista",
           "oczywiście",
           "owszem",
           "pewnie",
           "racja",
           "rozumie się",
           "rzecz jasna",
           "słusznie",
           "tak jest",
           "wiadomo",
           "właśnie",
           "z całą pewnością",
           "ano",
           "dokładnie",
           "dokładnie tak",
           "faktycznie",
           "istotnie",
           "no",
           "no tak",
           "w istocie",
           "w rzeczy samej",
           "zaiste",
           "aha",
           "no jasne",
           "prawda",
           "uhm",
           "no pewnie",
           "bez kwestii",
           "koniecznie",
           "obowiązkowo",
           "otóż to",
           "zgadza się"]
POS_NO = ['no',
          'n',
          "akurat",
          "ale gdzie tam",
          "ale skąd",
          "ani trochę",
          "broń Boże",
          "bynajmniej",
          "co znowu",
          "dobre sobie",
          "gdzież tam",
          "jeszcze czego",
          "myślałby kto",
          "nigdy w życiu",
          "skąd",
          "skądże znowu",
          "uchowaj Boże",
          "gdzie tam",
          "pod żadnym pozorem",
          "za nic w świecie",
          "za żadne skarby",
          "nie ma mowy",
          "niech Bóg broni",
          "niech ręka boska broni",
          "takiego",
          "wykluczone",
          "skądże",
          "w żadnym razie",
          "wcale",
          "wcale nie",
          "absolutnie nie",
          "nawet o tym nie myśl",
          "nic z tego",
          "nigdy",
          "przenigdy",
          "w życiu",
          "zupełnie nie",
          "nie ma o czym mówić",
          "nie może być mowy",
          "nie wchodzi w rachubę",
          "niestety",
          "niestety nie",
          "nie"
          ]
ACCEPTABLE_YESNO = POS_YES + POS_NO
THING = "animal"  # "persona", "cosa", "película"
RANDOM = False
NEW_AI = True
FAST = False
POINTS = True
MAXPOINTS = 5
MAXTRIES = 6

'''This is the animal-guesser configuration file
YES: word used on the database to represent YES
NO: word used on the database to represent NO
POS_YES and POS_NO: acceptable yes and no answers

THING: thing to guess. The original game is for animales, but can be used to play for
any thing or person. In order to be able to play the game, one must set up a new file called
"database_THING.json" with the following content:
#                                                  #
#       {QUESTION:{YES:[ANSWER],NO:[]}}            #
#                                                  #
where YES and NO are the variables specified in this file, and QUESTION and ANSWER
correspond to an initial question and answer, with quotes.

RANDOM: no "smart" question choosing, random instead.
#                                       #
#    possible values:  True o False     #
#                                       #

FAST: Enables fast answer discard. If the database does not contain the answer for a thing, discards it.
Less learning, but faster games.
#                                       #
#    possible values:  True o False     #
#                                       #

NEW_AI: Enables new question choosing system, using possible answers in current game, rather than all answers,
as it was before. Automatically disabled if used along RANDOM. Maybe too fast if used along FAST.
#                                       #
#    possible values:  True o False     #
#                                       #

POINTS: Enables point system. This allows the program to try to guess when some thing has enough points, rather than
discarding all the other possible answers.
#                                       #
#    possible values:  True o False     #
#                                       #

MAXPOINTS: Number of points needed to try and guess. (All things starts with 1 point)

MAXTRIES: Number of guessing tries before surrending.

'''
