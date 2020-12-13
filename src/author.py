from client import Client

import threading
import time
import random

TCP = [line.split(" ")[0] for line in open("TCP", 'r').read().split('\n')[:-1]]




class Author(Client):

    def __init__(self, host="localhost", proxy=7777, connection=None):
        Client.__init__(self, host, proxy)

    def bot(self, frequency, id = "AUTHOR"):
        self.message_box.start()
        self.consensus_call.start()
        self.register(id)

        init = True
        while init:
            mails = self.message_box.check()
            for request in mails.keys():
                if request in TCP:
                    for args in mails.get(request):
                        eval("self." + request + "(args)")
                else:
                    print("Requete Non reconnue :", request)
            if self.bag and self.blockchain:
                init = False
        size = len(self.blockchain)
        self.working = True
        while self.working:
            mails = self.message_box.check()
            for request in mails.keys():
                if request in TCP:
                    for args in mails.get(request):
                        eval("self." + request + "(args)")
                else:
                    print("Requete Non reconnue :", request)
            if size == len(self.blockchain):
                if self.bag:
                    letter = self.bag.pop()
                    self.sendLetter(letter)
                    size = size + 1
                else:
                    #print(self.blockchain)
                    print("letterbag vide, fin du processus")
                    self.leave(None)
        self.message_box.close()
        self.consensus_call.close()
        self.consensus_call.join()
        self.message_box.join()

    def run(self):
        self.working = True
        self.message_box.start()
        self.input_box.start()
        print("Pensez a vous enregistrer avec la commande : register $PUBLIC_KEY")
        while self.working:
            mails = self.message_box.check()
            for request in mails.keys():
                if request in TCP:
                    for args in mails.get(request):
                        eval("self." + request + "(args)")
                else:
                    print("Requete Non reconnue :", request)
            mails = self.input_box.check()
            for request in mails.keys():
                if request in TCP:
                    for args in mails.get(request):
                        eval("self." + request + "(args)")
                else:
                    print("Requete Non reconnue :", request)
        self.message_box.close()
        self.input_box.close()
        self.message_box.join()
        self.input_box.join()


if __name__ == "__main__" :
    print(">>")
    Author(proxy=int(open("proxy").read())).bot(1,str(random.randint(1,1000)).encode())
    print("<<")