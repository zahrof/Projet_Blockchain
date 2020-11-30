import hashlib
import copy
import letter 

class Word(object):
    def __init__(self, letters, period, head, author):

        self.word = letters
        self.period = period
        self.author = copy.deepcopy(author)
        self.head = copy.deepcopy(head)

        self._m = hashlib.sha256()
        [self._m.update(letter.signature) for letter in letters]
        self._m.update(author)
        self._m.update(head)
        self._m.update(bin(period).encode())

        self.signature = self._m.digest()

    def __str__(self):  # changer str vers un toJson ?
        return """
        letter: {}, period: {},
        head: {},
        author: {},
        signature: {}
        """.format(self.word, self.period, self.head, self.author, self.signature)

    def __repr__(self):
        return """
        letter: {}, period: {},
        head: {},
        author: {},
        signature: {}
        """.format(self.word, self.period, self.head, self.author, self.signature)

    def getStr(self):
        return ('').join([l.letter.decode('utf-8') for l in self.word])
        
       
exemple1 = Word([letter.exemple1, letter.exemple2], 0, b"""123456789""", b"""cafe""")
# exemple1.getStr() renvoie 'ab' 
