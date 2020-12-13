from client import Client
from dictionnary import Dictionnary
from consensus import str_score
from word import Word
from letter import Letter

import random
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
        self.consensus_call.start()
        self.register(id)
        cend = 0
        init = True
        while init:
            mails = self.message_box.check()
            for request in mails.keys():
                print(request)
                if request in TCP:
                    for args in mails.get(request):
                        eval("self." + request + "(args)")
                else:
                    print("Requete Non reconnue :", request)
            if self.bag and self.blockchain:
                init = False
        research = Searching(self.letters_pool.getCopy(), self.dictionnary)
        research.start()
        t = time.time()
        self.working = True
        while self.working:
            mails = self.message_box.check()
            for request in mails.keys():
                if request in TCP:
                    for args in mails.get(request):
                        if(request == "receiveLetter"):
                            print("Letter reçu:", eval(args).letter.decode("utf-8"))
                        elif(request == "receiveWord"):
                            print("Mot proposé:", eval(args).getStr())
                        eval("self." + request + "(args)")
                else:
                    print("Requete Non reconnue :", request)
            if time.time() - t > frequency:
                letters = research.stop()
                research.join()
                if letters:
                    if letters[0].period == len(self.blockchain):
                        cend = 0
                        self.sendWord(Word(letters, len(self.blockchain), self.blockchain[-1].head, self.public_key))
                else:
                    print("En attente de lettres...")
                    cend += 1
                    if cend == 10:
                        print("time out, fermeture du processus")
                        self.leave(None)
                research = Searching(self.letters_pool.getCopy(), self.dictionnary)
                research.start()
                t = time.time()
        self.message_box.close()
        self.consensus_call.close()
        self.message_box.join()
        self.consensus_call.join()




class Searching(threading.Thread):

    def __init__(self, authorLetter, dictionnaire):
        threading.Thread.__init__(self)
        self.authorLetter = authorLetter
        self.dictionnaire = dictionnaire
        self.result = None
        self.working = False

    def getBest(self, arr):
        bestS = 0
        bestE = None
        for (word, letter) in arr:
            temp = str_score(word)
            if temp > bestS:
                bestS = temp
                bestE = (word, letter)
        return bestE

    def stop(self):
        self.working = False
        if self.result:
            _, self.result = self.result
        return self.result

    def run(self):
        self.working = True
        isVis = set()
        letterUse = list()
        mem = list()
        for word in self.dictionnaire:
            word = random.choice(self.dictionnaire)
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
        self.result = self.getBest(mem)


if __name__ == "__main__" :
    print(">>")
    Politician(proxy=int(open("proxy").read()), paths=["./../dict/dict_100000_1_10.txt"]).bot(4, str(random.randint(1,1000)).encode())
    print("<<")