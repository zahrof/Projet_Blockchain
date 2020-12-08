import socket
import select
import json
import threading
import time


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
            try :
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

    def __init__(self, host = "localhost", proxy = 7777, connection = None):
        if not connection:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((host, proxy))
            print("Connexion établie avec le serveur sur le port {}".format(proxy))
        else : self.connection = connection
        self.message_box = MessageBox(self.connection)
        self.input_box = InputBox()
        self.working = False
        self.bag = list()
        self.public_key = ""

    def send(self, request, message):
        self.connection.send(str({request : message}).encode())

    def talk(self, message):
        self.send("talk", message)

    def word(self, word):
        self.send("word", word.serialiaze())

    def mot(self, mot):
        w = eval(mot)

    def leave(self, _):
        self.send("leave", None)
        self.working = False

    def message(self, args):
        who = args[0]
        message = args[1]
        print(who,":",message)

    def system(self, message):
        self.message(["system", message])

    def letters_bag(self, bag):
        self.bag = bag

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
        Client.__init__(self,connection=connection)


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
    Client(proxy = 7779).isAuthor().run()
    print("END")

