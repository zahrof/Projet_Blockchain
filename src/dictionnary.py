class Dictionnary(list):

    def read(self, path):
        with open(path) as file:
            self.extend(file.read().split('\n')[:-1])

    def readAll(self, iterable):
        for path in iterable:
            self.read(path)