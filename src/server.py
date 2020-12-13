import secrets
import socket
import select
import threading
import random

from boxes import MessageBox, InputBox
from word import Word

TCP = [line.split(" ")[0] for line in open("TCP", 'r').read().split('\n')[:-1]]

lock_clients = threading.RLock()
lock_printer = threading.RLock()


# Il faut signer les lettres du pool initial pour empecher les joueurs d'en generer
def letters_bag():
    return [chr(secrets.randbelow(26) + ord('a')).encode() for _ in range(5)]


class Client(threading.Thread):

    def __init__(self, server, client_accept):
        threading.Thread.__init__(self)
        self.server = server
        self.client, self.infos = client_accept
        self.message_box = MessageBox(self.client)
        self.working = False
        self.public_key = ""
        self.requests = {}
        self.lock_send = threading.RLock()
        self.kicked = set()
        self.lock_kick = threading.RLock()

    def send(self, request, args):
        with self.lock_send:
            self.client.send(str({request: args}).encode())

    def sendAll(self, request, args):
        with lock_clients:
            for client in self.server.clients.values():
                client.send(request, args)

    def sendTo(self, dest, request, args):
        #with lock_clients:
        server.clients[dest].send(request, args)

    def register(self, public_key):
        if self.public_key == "":
            with lock_clients:
                self.server.clients[public_key[0]] = self
                self.public_key = public_key[0]
                if not self.server.head:
                    init = Word(b"", 0, b"", self.public_key).serialize()
                    self.server.head = self
                else:
                    init = Word(b"", 0, b"", self.server.head.public_key).serialize()
            self.send("letters_bag", letters_bag())
            self.send("initial_block", init)
            self.server.display("new client :", self.infos, self.public_key)
            self.server.display("init", init)
        else:
            self.send("system", "Requete ignoree : vous etes deja enregistre.")



    def getVerif(self, newblock):
        self.sendAll("getVerif", (self.public_key, newblock))

    def retVerif(self, args):
        to, ret = args
        self.server.display("RETVERIF", ret)
        self.sendAll("retVerif", (len(server.clients.keys()), ret, to))

    def sendWord(self, word):
        with lock_clients:
            for client_s in self.server.clients.values():
                client_s.send("receiveWord", word)

    def sendLetter(self, letter):
        #self.server.display(self.public_key, "send letter :", letter)
        with lock_clients:
            for client_s in self.server.clients.values():
                client_s.send("receiveLetter", letter)

    def talk(self, message):
        #self.server.display(message)
        with lock_clients:
            for client_s in self.server.clients.values():
                client_s.send("message", [self.public_key, message])

    def kick(self, to):
        with lock_clients:
            bad_guy = server.clients.get(to, None)
            if bad_guy:
                with bad_guy.lock_kick:
                    bad_guy.kicked.add(self)
                    if len(bad_guy.kicked) >= (len(self.server.clients.keys())):
                        self.sendAll("system", "leader banned")
                        bad_guy.leave(None)
        with lock_clients:
            if len(self.server.clients) > 0:
                random.choice(list(self.server.clients.values())).send("consensus", True)



    def leave(self, _):
        with lock_clients:
            del server.clients[self.public_key]
            if len(server.clients.keys()) == 0:
                server.working = False
        self.send("system", None)
        self.client.close()
        self.working = False

    def run(self):
        self.working = True
        self.message_box.start()
        mails = {}
        while self.working and self.server.working:
            news = self.message_box.check()
            for key in news.keys():
                mails[key] = mails.get(key, []) + news[key]
            if self.public_key == "":
                if not mails.keys().__contains__("register"):
                    #self.send("system", "En attente d'enregistrement")
                    continue
                else:
                    self.register(mails["register"])
            for request in mails.keys():
                if request in TCP:
                    if request == "register": continue
                    for args in mails.get(request):
                        eval("self." + request + "(args)")
                else:
                    print("Requete Non reconnue :", request)
            mails.clear()
        self.message_box.close()
        self.server.display(self.public_key, "est parti.")
        self.client.close()


class Server(threading.Thread):

    def __init__(self, host, proxy):
        threading.Thread.__init__(self)
        self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_connection.bind((host, proxy))
        self.main_connection.listen(5)
        self.lock_display = threading.RLock()
        self.display("Le serveur écoute à present sur le port {}".format(proxy))
        self.host, self.proxy = host, proxy
        self.working = False
        self.head = None
        self.head
        self.clients = {}

    def display(self, *message):
        with self.lock_display:
            print(" ".join([str(m) for m in message]))

    def accept_users(self):
        connection_requests, _, _ = select.select([self.main_connection], [], [], 0.05)
        for connection in connection_requests:
            Client(self, connection.accept()).start()

    def run(self):
        self.working = True
        while self.working:
            self.accept_users()
        self.display("Fin!")
        self.main_connection.close()


if __name__ == "__main__":
    server = Server('', int(open("proxy").read()))
    server.start()
