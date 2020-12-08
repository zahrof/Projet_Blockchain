from word import *
import logging


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
    ws = WordStore([exemple0])  
    print([i for i in ws])