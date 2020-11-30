
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
    return sum([scrab_score(c) for c in w.getStr()])

# fitness st word =



#let head ?level (st : Store.word_store) =

