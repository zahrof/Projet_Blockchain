import secrets
import socket
import select
import threading

from boxes import MessageBox

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

    def send(self, request, args):
        with self.lock_send:
            self.client.send(str({request: args}).encode())

    def register(self, public_key):
        self.server.display("public_key", public_key)
        if self.public_key == "":
            with lock_clients:
                self.server.clients[public_key[0]] = self
                self.public_key = public_key[0]
            self.client.send(str({"letters_bag": letters_bag()}).encode())
            self.server.display("new client :", self.infos, self.public_key)
        else:
            self.send("system", "Requete ignoree : vous etes deja enregistre.")

    def sendWord(self, word):
        self.server.display(word)
        with lock_clients:
            for client_s in self.server.clients.values():
                client_s.send("receiveWord", word)

    def sendLetter(self, letter):
        self.server.display(self.public_key, "send letter :", letter)
        with lock_clients:
            for client_s in self.server.clients.values():
                client_s.send("receiveLetter", letter)

    def talk(self, message):
        self.server.display(message)
        with lock_clients:
            for client_s in self.server.clients.values():
                client_s.send("message", [self.public_key, message])

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

        while self.working and self.server.working:
            mails = self.message_box.check()
            if self.public_key == "":
                if not mails.keys().__contains__("register"):
                    self.send("system", "Requetes ignorees, vous devez vous enregistrer.")
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
    server = Server('', 9999)
    server.start()
