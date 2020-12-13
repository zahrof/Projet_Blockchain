from word import *
import logging
import copy

class WordStore(object):
    def add_word(self, word):
        if not word.check_signature():
            logging.warning("""Incorrect Word Signature {}, 
            word not added to word store""".format(word.getStr()))

        # crypter ici ?
        self._hashT[word] = word
    
    def __init__(self, iter = None, check_sign = True):
        """
        iter: itérable de mot à ajouter, potentiellement vide
        /!\ on a pas encore de crypto (peut-être pas nécessaire)
        """
        # gen une clé RSA ou _hashT ?

        self.check_sign = check_sign
        self._hashT = dict()
        if iter is not None:
            for elem in iter:
                self.add_word(elem)
    
    def get_word(self, word):
        # crypter ici ?
        return self._hashT.get(word)

    def __len__(self):
        return len(self._hashT)

    def __iter__(self):
        return self._hashT.__iter__()

if __name__ == "__main__":
    ws = WordStore([wexemple0])  
    print([i for i in ws])

class LetterStore(object):
    def add_letter(self, letter):
        #check_signature into logging.warning
        l = letter.letter.decode("utf-8")
        if len(l) != 1 or l not in 'azertyuiopqsdfghjklmwxcvbn':
            logging.warning(l + " is not a valid letter")
            return
        self._hashT[l].append(letter)
        
    def __len__(self):
        return sum([len(x) for x in self._hashT.values()])    
    
    def __init__(self, iter = None, check_sign = True):
        """
        iter: itérable de letter à ajouter, potentiellement vide
        /!\ on a pas encore de crypto (peut-être pas nécessaire)
        """
        self.check_sign = check_sign
        self._hashT = dict()
        for i in 'azertyuiopqsdfghjklmwxcvbn':
            self._hashT[i] = list()

        if iter is not None:
            for elem in iter:
                self.add_letter(elem)
    def getCopy(self):
        ret = dict()
        for i in 'azertyuiopqsdfghjklmwxcvbn':
            ret[i] = self._hashT[i] * 1
        return ret

    def purge(self):
        for i in 'azertyuiopqsdfghjklmwxcvbn':
            self._hashT[i] = list()

