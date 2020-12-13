import socket
import select
import json
import threading
import time
import random
from asyncio import Event
import ed25519

from dictionnary import Dictionnary
from letter import Letter
from client_utils import containsWordBestFit
from store import LetterStore, WordStore
from word import Word
from boxes import MessageBox, InputBox, ConsensusCall
from consensus import word_score, bestWord
from chain import Blockchain

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
        self.consensus_call = ConsensusCall(self.message_box)
        self.working = False
        self.bag = list()
        self.blockchain = Blockchain()
        self.letters_pool = LetterStore()
        self.word_pool = WordStore()
        self.tret = 0
        self.fret = 0
        self.tmpblock = None
        self._privateKey, self.public_key = ed25519.create_keypair()
        self.public_key = self.public_key.to_bytes()

    def send(self, request, message):
        self.connection.send(str({request: message}).encode())

    def initial_block(self, word):
        self.blockchain.append(eval(word))

    def consensus(self, _):
        if(len(self.word_pool) == 0):
            return # Nothing
        if self.public_key == self.blockchain[-1].politician_id or _:
            self.tret, self.fret = 0, 0
            self.send("getVerif", bestWord(self.word_pool).serialize())

    def getVerif(self, args):
        to, tmpblock = args
        self.tmpblock = eval(tmpblock)
        if [l for l in self.tmpblock.letters if l.period != self.tmpblock.period or not l.check_signature()] or not self.tmpblock.check_signature():
            self.send("retVerif", (to, False))
        else:
            authors = [l.author for l in self.tmpblock.letters]
            vote = len(authors) == len(set(authors)) and self.word_pool.contains(self.tmpblock) and word_score(self.tmpblock) >= word_score(bestWord(self.word_pool))
            self.send("retVerif", (to, vote))

    def retVerif(self, args):
        if self.tmpblock:
            n, ret, to = args
            if ret: self.tret += 1
            else: self.fret += 1
            if self.tret >= n/2:
                self.tret, self.fret = 0, 0
                self.blockchain.append(self.tmpblock)
                self.letters_pool.purge(len(self.blockchain))
                self.word_pool.purge(len(self.blockchain))
                self.tmpblock = None
                print("blockchain :", self.blockchain)
            elif self.fret >= n/2:
                self.tret, self.fret = 0, 0
                self.tmpblock = None
                self.send("kick", to)


    def talk(self, message):
        self.send("talk", message)

    def sendWord(self, letters):
        self.send("sendWord", Word(letters, len(self.blockchain), self.blockchain[-1].head, self.public_key, pkey=self._privateKey).serialize())

    def receiveWord(self, mot):
        w = eval(mot)
        if w.period == len(self.blockchain):
            self.word_pool.add(w)

    def sendLetter(self, letter):
        print(str(letter)[2], " a été envoyé")
        self.send("sendLetter", Letter(letter, len(self.blockchain), self.blockchain[-1].head, self.public_key, pkey=self._privateKey).serialize())

    def blockchain(self, chain):
        # On peut rajouter un check complet de la BC pour la sécurité
        self.blockchain = chain

    def receiveLetter(self, letter):
        self.letters_pool.add_letter(eval(letter))


    def leave(self, _):
        self.send("leave", None)
        self.working = False

    def message(self, args):
        who = args[0]
        message = args[1]

    def system(self, message):
        self.message(["system", message])

    def letters_bag(self, bag):
        self.bag = bag

    def register(self, public_key):
        self.send("register", self.public_key)


if __name__ == "__main__":
    None
