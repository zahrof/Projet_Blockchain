from word import *
import logging
import copy

class WordStore(set):

    def __init__(self, iter = list(), check_sign = True):
        """
        iter: itérable de mot à ajouter, potentiellement vide
        /!\ on a pas encore de crypto (peut-être pas nécessaire)
        """
        # gen une clé RSA ou _hashT ?
        set.__init__(self)
        self.store = set(iter)
        self.s = set()

    def contains(self, item):
        for e in self:
            if e.signature == item.signature:
                return True
        return False

    def purge(self, period):
        WordStore.__init__(self, [x for x in self if x.period >= period])

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



    def purge(self, period):
        for i in 'azertyuiopqsdfghjklmwxcvbn':
            self._hashT[i] = [e for e in self._hashT[i] if e.period >= period]

