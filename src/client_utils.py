from letter import *
from consensus import *
from store import *

def read_dict(str):
    with open(str) as f:
        return [l for l in f.readlines()]

# fun: list letter + dict -> None ou mot

def containsWord(authorLetter, dictionnaire):
    isVis = set()
    letterUse = list()
    for word in dictionnaire: 
        for l in word:
            cand = False
            for letter in authorLetter[l]:
                if letter.author not in isVis:
                    isVis.add(letter.author)
                    letterUse.append(letter)
                    cand = True
            if cand == False:
                # on a pas trouvé de lettre candidate donc on reset les mémoires
                letterUse = list()
                isVis = set()
                break
        if len(letterUse) == len(word):
            return (word, letterUse)
    return None

def containsWordBestFit(authorLetter, dictionnaire):
    def getBest(arr):
        bestS = 0
        bestE = None
        for (word, letter) in arr:
            temp = str_score(word)
            if temp > bestS:
                bestS = temp
                bestE = (word, letter) 
        return bestE

    isVis = set()
    letterUse = list()
    mem = list()
    for word in dictionnaire: 
        for l in word:
            cand = False
            for letter in authorLetter[l]:
                if letter.author not in isVis:
                    isVis.add(letter.author)
                    letterUse.append(letter)
                    cand = True
            if cand == False:
                # on a pas trouvé de lettre candidate donc on reset les mémoires
                letterUse = list()
                isVis = set()
                break
        if len(letterUse) == len(word):
            mem.append(((word, letterUse)))
            letterUse = list()
            isVis = set()    
            
    return getBest(mem)

if __name__ == "__main__":

    f1 = read_dict("../dict/dict_100000_5_15.txt")
    print(len(f1))

    authorL = LetterStore([lexemple1, lexemple2, lexemple3])
    authorLetterEx = authorL.getCopy()

    authorLetterEx['a'].append(lexemple1)
    authorLetterEx['b'].append(lexemple2)
    authorLetterEx['b'].append(lexemple3)
    print(containsWord(authorLetterEx, ['c', 'bb', 'ab']))        # ab
    print(containsWord(authorLetterEx, ['c', 'a', 'ab']))         # a 
    print(containsWord(authorLetterEx, ['c', 'bb', 'ab', 'bab'])) # ab
    print(containsWord(authorLetterEx, ['c', 'bb', 'bab'])) # None 
    print(containsWord(authorLetterEx, ['c', 'bb']))        # None 

    print(containsWordBestFit(authorLetterEx, ['c', 'bb', 'ab']))        # ab
    print(containsWordBestFit(authorLetterEx, ['c', 'a', 'ab']))         # ab
    print(containsWordBestFit(authorLetterEx, ['c', 'bb', 'ab', 'bab'])) # ab
    print(containsWordBestFit(authorLetterEx, ['c', 'bb', 'bab'])) # None 
    print(containsWordBestFit(authorLetterEx, ['c', 'bb']))        # None 