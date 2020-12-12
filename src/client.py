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
from boxes import MessageBox, InputBox

from consensus import str_score

TCP = [line.split(" ")[0] for line in open("TCP", 'r').read().split('\n')[:-1]]

lock_msg = threading.RLock()





class Client:

    def __init__(self, host="localhost", proxy=7777):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((host, proxy))
        print("Connexion établie avec le serveur sur le port {}".format(proxy))
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
        print("sendW", word)
        self.send("sendWord", word.serialize())

    def receiveWord(self, mot):
        w = eval(mot)
        print("recuW", w)
        if w.period == len(self.blockchain):
            print(w)
            self.blockchain.append(w)

    def sendLetter(self, letter):
        print("sendL", letter)
        self.send("sendLetter", Letter(letter, len(self.blockchain), self.blockchain[-1].head, self.public_key).serialize())

    def receiveLetter(self, letter):
        print("recuL", letter)
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
        print("bag", bag)
        self.bag = bag

    def register(self, public_key):
        print(public_key)
        if self.public_key == "":
            self.public_key = public_key
            self.send("register", public_key)
        else:
            print("Vous êtes deja enregistré")









if __name__ == "__main__":
    None
