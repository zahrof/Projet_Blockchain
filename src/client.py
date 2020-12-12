import socket
import select
import json
import threading
import time
import random
from asyncio import Event

from dictionnary import Dictionnary
from letter import Letter
from client_utils import containsWordBestFit
from store import LetterStore
from word import Word

from consensus import str_score

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
        self.blockchain = [Word(b"", 0, b"", b"init")]
        self.letters_pool = LetterStore()

    def send(self, request, message):
        self.connection.send(str({request: message}).encode())

    def talk(self, message):
        self.send("talk", message)

    def sendWord(self, word):
        self.send("sendWord", word.serialize())

    def receiveWord(self, mot):
        w = eval(mot)
        print(w)
        if w.period == len(self.blockchain):
            print(w)
            self.blockchain.append(w)

    def sendLetter(self, letter):
        self.send("sendLetter", Letter(letter, len(self.blockchain), self.blockchain[-1].head, self.public_key))

    def receiveLetter(self, letter):
        self.letters_pool.add_letter(eval(letter))


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
        self.bag = bag

    def register(self, public_key):
        if self.public_key == "":
            self.public_key = public_key
            self.send("register", public_key)
        else:
            print("Vous êtes deja enregistré")









if __name__ == "__main__":
    None
