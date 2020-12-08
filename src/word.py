import hashlib
import copy
import letter 

class Word(object):
    def __init__(self, letters, period, head, politician_id):

        self.word = letters
        self.period = period
        self.politician_id = politician_id
        self.head = head

        self._m = hashlib.sha256()
        [self._m.update(letter.signature) for letter in letters]
        self._m.update(politician_id)
        self._m.update(head)
        self._m.update(bin(period).encode())

        self.signature = self._m.digest()

    def __str__(self):  # changer str vers un toJson ?
        return """
        letter: {}, period: {},
        head: {},
        politician_id: {},
        signature: {}
        """.format(self.word, self.period, self.head, self.politician_id, self.signature)

    def __repr__(self):
        return """
        letter: {}, period: {},
        head: {},
        politician_id: {},
        signature: {}
        """.format(self.word, self.period, self.head, self.politician_id, self.signature)

    def getStr(self):
        return ('').join([l.letter.decode('utf-8') for l in self.word])

    def check_signature(self):
        m = hashlib.sha256()
        [m.update(letter.signature) for letter in self.letters]
        m.update(self.politician_id)
        m.update(self.head)
        m.update(bin(self.period).encode())
        return (self.signature == m.digest())
        

###     pour les tests  ###
wexemple0 = Word([letter.lexemple1, letter.lexemple1], 0, b"""123456789""", b"""cafe""")
wexemple1 = Word([letter.lexemple1, letter.lexemple2], 0, b"""123456789""", b"""cafe""")
    

if __name__ == "__main__":
    print(wexemple1.getStr())
    print(wexemple1.check_signature())

    print("on touche au mot")
    wexemple1.period = 1
    print(wexemple1.check_signature())
