from client import Client
from dictionnary import Dictionnary
from consensus import str_score
from word import Word

import threading
import time

TCP = [line.split(" ")[0] for line in open("TCP", 'r').read().split('\n')[:-1]]


class Politician(Client):

    def __init__(self, host="localhost", proxy=7777, paths = list()):
        Client.__init__(self, host, proxy)
        self.dictionnary = Dictionnary()
        self.dictionnary.readAll(paths)

    def searchWord(self):
        return None


    def bot(self, frequency, id = "POLITICIAN"):
        self.message_box.start()
        self.register(id)
        research = Searching(self.letters_pool.getCopy(), self.dictionnary)
        research.start()
        t = time.time()
        self.working = True
        while self.working:
            mails = self.message_box.check()
            for request in mails.keys():
                if request in TCP:
                    for args in mails.get(request):
                        eval("self." + request + "(args)")
                else:
                    print("Requete Non reconnue :", request)
            if time.time() - t > frequency:
                letters = research.stop()
                research.join()
                if letters:
                    self.sendWord(Word(letters, len(self.blockchain), self.blockchain[-1].head, self.public_key))
                research = Searching(self.letters_pool.getCopy(), self.dictionnary)
                research.start()
                t = time.time()




class Searching(threading.Thread):

    def __init__(self, authorLetter, dictionnaire):
        threading.Thread.__init__(self)
        self.authorLetter = authorLetter
        self.dictionnaire = dictionnaire
        self.result = None
        self.working = False

    def getBest(self, arr):
        bestS, bestE = 0, None
        for (word, letter) in arr:
            temp = str_score(word)
            if temp > bestS:
                bestS = temp
                bestE = (word, letter)
        return bestE

    def stop(self):
        self.working = False
        return self.result

    def run(self):
        self.working = True
        isVis = set()
        letterUse = list()
        mem = list()
        for word in self.dictionnaire:
            if not self.working:
                break
            for l in word:
                cand = False
                for letter in self.authorLetter[l]:
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
        _, self.result = self.getBest(mem)


if __name__ == "__main__" :
    print(">>")
    Politician(proxy=9999, paths=["./../dict/dict_26_1_1.txt"]).bot(1, b"P1")
    print("<<")