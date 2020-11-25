import secrets
import socket
import select
import threading
import json



TCP = [line.split(" ")[0] for line in open("TCP", 'r').read().split('\n')[:-1]]

lock_clients = threading.RLock()
lock_printer = threading.RLock()


def letters_bag():
    return [chr(secrets.randbelow(26) + ord('a')) for _ in range(50)]


class Client(threading.Thread):

    def __init__(self, server, client_accept):
        threading.Thread.__init__(self)
        self.server = server
        self.client, self.infos = client_accept
        self.working = False
        self.public_key = ""
        self.requests = {}
        self.lock_send = threading.RLock()

    def register(self, public_key):
        if self.public_key == "":
            with lock_clients:
                Server.clients[public_key] = self
                self.public_key = public_key
                self.client.send(str({"letters_bag" : letters_bag()}).encode())
                with lock_printer:
                    print("new client :", self.infos, self.public_key)
        else:
            with self.lock_send:
                self.client.send(str({"system" : "Requete ignoree : vous etes deja enregistre."}).encode())


    def talk(self, message):
        with lock_printer :
            print(message)
        with lock_clients:
            for client_s in self.server.clients.values():
                with client_s.lock_send:
                    client_s.Client.send(str({"message" : [self.public_key, message]}).encode())

    def leave(self, _):
        with lock_clients:
            del Server.clients[self.public_key]
            if len(Server.clients.keys()) == 0:
                Server.working = False
        self.client.close()
        self.working = False

    def run(self):
        self.working = True

        while self.working and self.server.working:
            try :
                requests = eval(self.client.recv(1024).decode())
            except SyntaxError:
                continue
            if self.public_key == "":
                if "register" in requests.keys():
                    self.register(requests["register"])
                else: # pas besoin de lock, personne ne vous vois
                    self.client.send(str({"system" : "Requetes ignore, vous devez vous enregistrer."}).encode())
            else:
                for request in requests.keys():
                    if self.working == False:
                        break
                    elif request in TCP:
                        eval("self." + request + "(requests[request])")
                    else:
                        with self.lock_send:
                            self.client.send(({"system" : "Requete Non Reconnue : " + request}).encode())
        with lock_printer:
            print(self.public_key, "est partis.")
        self.client.close()


class Server(threading.Thread):

    def __init__(self, host, proxy):
        threading.Thread.__init__(self)
        self.main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main_connection.bind((host, proxy))
        self.main_connection.listen(5)
        with lock_printer:
            print("Le serveur écoute à present sur le port {}".format(proxy))
        self.host, self.proxy = host, proxy
        self.working = False
        self.clients = {}

    def accept_users(self):
        connection_requests, _, _ = select.select([self.main_connection], [], [], 0.05)
        for connection in connection_requests:
            Client(self, connection.accept()).start()

    def run(self):
        self.working = True
        while self.working:
            self.accept_users()
        with lock_printer:
            print("Fin!")
        self.main_connection.close()


if __name__ == "__main__":
    server = Server('', 1234)
    server.start()
