import threading


class MessageBox(threading.Thread):

    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection
        self.box = dict()
        self.lock_box = threading.RLock

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