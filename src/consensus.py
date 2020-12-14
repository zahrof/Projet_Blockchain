from store import *
from word import *

def scrab_score(c): 
    # https://fr.wikipedia.org/wiki/Lettres_du_Scrabble#Français
    if c in 'eainorstul':
        return 1
    elif c in 'dmg':
        return 2
    elif c in 'bcp':
        return 3
    elif c in 'fhv':
        return 4
    elif c in 'jq':
        return 8
    return 10

# word_score { word; _ } : int =

def word_score(w):
    #mémoïser ?
    return sum([scrab_score(c) for c in w.getStr()])

def str_score(string):
    #mémoïser ?
    return sum([scrab_score(c) for c in string])

def bestWord(wordS):
    return max(wordS, key = word_score)

def cons(word, wordS):
    autS = set()
    [autS.add(l.author) for l in word.word]
    if(len(word.word) != len(autS)):
        return False # le mot contient plusieurs lettres du même auteur
    return wordS.get_word(word) is not None and word_score(word) >= word_score(bestWord(wordS))

#let head ?level (st : Store.word_store) =
 
if __name__ == "__main__":
    wS = WordStore([wexemple0, wexemple1])
    print(bestWord(wS))
    print(cons(wexemple1, wS))