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
        letters = self.word 
        period = self.period
        politician_id = self.politician_id 
        head = self.head 

        m = hashlib.sha256()
        [m.update(letter.signature) for letter in letters]
        m.update(politician_id)
        m.update(head)
        m.update(bin(period).encode())

        return (self.signature == m.digest())
        

###     pour les tests  ###
exemple0 = Word([letter.exemple1, letter.exemple1], 0, b"""123456789""", b"""cafe""")
exemple1 = Word([letter.exemple1, letter.exemple2], 0, b"""123456789""", b"""cafe""")
    

if __name__ == "__main__":
    print(exemple1.getStr())
    print(exemple1.check_signature())

    print("on touche au mot")
    exemple1.period = 1
    print(exemple1.check_signature())
