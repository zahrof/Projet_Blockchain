import hashlib
import copy

class Letter(object):
    def __init__(self, letter, period, head, author):
        assert(len(letter) == 1)
        self.letter = letter
        self.period = period
        self.author = copy.deepcopy(author)
        self.head = copy.deepcopy(head)

        self._m = hashlib.sha256()
        self._m.update(letter)
        self._m.update(author)
        self._m.update(head)
        self._m.update(bin(period).encode())

        self.signature = self._m.digest()

    def __str__(self):
        return """
        letter: {}, period: {},
        head: {},
        author: {},
        signature: {}
        """.format(self.letter, self.period, self.head, self.author, self.signature)

    def __repr__(self):
        return str(self)
        
       
exemple1 = Letter(b"a", 0, b"""123456789""", b"""cafe""")
exemple2 = Letter(b"b", 0, exemple1.signature, b"""456""")
