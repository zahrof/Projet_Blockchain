from client import Client

import threading
import time

TCP = [line.split(" ")[0] for line in open("TCP", 'r').read().split('\n')[:-1]]


class Author(Client):

    def __init__(self, host="localhost", proxy=7777, connection=None):
        Client.__init__(self, host, proxy)

    def bot(self, frequency, id = "AUTHOR"):
        self.message_box.start()
        self.register(id)
        t = time.time()
        self.working = True
        size = len(self.blockchain)
        while self.working:
            mails = self.message_box.check()
            for request in mails.keys():
                if request in TCP:
                    for args in mails.get(request):
                        eval("self." + request + "(args)")
                else:
                    print("Requete Non reconnue :", request)
            if size == len(self.blockchain):
                print(size, len(self.blockchain))
                if self.bag:
                    letter = self.bag.pop()
                    print(letter)
                    self.sendLetter(letter)
                else:
                    print(self.blockchain)
                    self.leave(None)
                t = time.time()
        self.message_box.close()
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
    Author(proxy=7783).bot(1,b"A1")
    print("<<")