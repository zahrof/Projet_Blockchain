import socket
import select
import json
import threading
import time
import random

from letter import Letter

TCP = [line.split(" ")[0] for line in open("TCP", 'r').read().split('\n')[:-1]]

lock_msg = threading.RLock()


class MessageBox(threading.Thread):

    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection
        self.box = dict()
        self.lock_box = threading.RLock()
        self.working = False

    def close(self):
        self.working = False

    def check(self):
        with self.lock_box:
            mails = self.box.copy()
            self.box.clear()
        return mails

    def add(self, requests):
        for request in requests.keys():
            with self.lock_box:
                self.box[request] = self.box.get(request, []) + [requests.get(request)]

    def run(self):
        self.working = True
        while self.working:
            try:
                self.add(eval(self.connection.recv(1024).decode()))
            except SyntaxError:
                pass


class InputBox(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.box = dict()
        self.lock_box = threading.RLock()
        self.working = False

    def close(self):
        self.working = False

    def check(self):
        with self.lock_box:
            mails = self.box.copy()
            self.box.clear()
        return mails

    def add(self, message):
        message = message.strip(" ")
        S = message.split()
        with self.lock_box:
            self.box[S[0]] = self.box.get(S[0], []) + [" ".join(S[1:])]
        if S[0] == "leave":
            self.working = False

    def run(self):
        self.working = True
        while self.working:
            self.add(input(""))


class Client:

    def __init__(self, host="localhost", proxy=7777, connection=None):
        if not connection:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((host, proxy))
            print("Connexion établie avec le serveur sur le port {}".format(proxy))
        else:
            self.connection = connection
        self.message_box = MessageBox(self.connection)
        self.input_box = InputBox()
        self.working = False
        self.bag = list()
        self.public_key = ""
        self.blockchain = list()

    def send(self, request, message):
        self.connection.send(str({request: message}).encode())

    def talk(self, message):
        self.send("talk", message)

    def sendWord(self, word):
        self.send("sendWord", word.serialize())

    def receiveWord(self, mot):
        w = eval(mot)
        if w.period == len(self.blockchain):
            print(w)
            self.blockchain.append(w)

    def sendLetter(self, letter):
        self.send("sendLetter", letter)

    def receiveLetter(self, letter_encoded):
        letter = eval(letter_encoded)
        print(letter)

    def leave(self, _):
        self.send("leave", None)
        self.working = False

    def message(self, args):
        who = args[0]
        message = args[1]
        print(who, ":", message)

    def system(self, message):
        self.message(["system", message])

    def letters_bag(self, bag):
        self.bag = [Letter(l.encode(), 0, b"""123456789""", b"""cafe""") for l in bag]

    def register(self, public_key):
        if self.public_key == "":
            self.public_key = public_key
            self.send("register", public_key)
        else:
            print("Vous êtes deja enregistré")

    def isAuthor(self):
        return Author(self.connection)

    def isPolitician(self):
        return Politician(self.connection)

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


class Author(Client):

    def __init__(self, connection):
        Client.__init__(self, connection=connection)

    def bot(self, frequency):
        self.message_box.start()
        self.register("Claire")
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
            if time.time()-t > frequency:
                if self.bag:
                    letter = self.bag.pop()
                    print(letter)
                    self.sendWord(letter)
                else:
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


class Politician(Client):

    def __init__(self, connection):
        Client.__init__(self, connection=connection)

    def run(self):
        None


if __name__ == "__main__":
    print("START")
    Client(proxy=7782).isAuthor().bot(1)
    print("END")
