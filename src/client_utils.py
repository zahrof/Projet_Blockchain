from letter import *

def read_dict(str):
    f = open(str) # peut lever une Exception
    lst = [l for l in f.readlines()]
    f.close()
    return lst


f1 = read_dict("../dict/dict_100000_5_15.txt")
print(len(f1))

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


authorLetterEx = dict()
for i in 'azertyuiopqsdfghjklmwxcvbn':
    authorLetterEx[i] = list()
authorLetterEx['a'].append(exemple1)
authorLetterEx['b'].append(exemple2)
authorLetterEx['b'].append(exemple3)
print(containsWord(authorLetterEx, ['c', 'bb', 'ab']))
print(containsWord(authorLetterEx, ['c', 'bb', 'bab'])) # None 
print(containsWord(authorLetterEx, ['c', 'bb']))        # None 
