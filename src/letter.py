import hashlib
import copy

class Letter(object):
    def __init__(self, letter, period, head, author):
        assert(len(letter) == 1)
        self.letter = letter
        self.period = period
        self.author = author
        self.head = head

        self._m = hashlib.sha256()
        self._m.update(letter)
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
        """.format(self.letter, self.period, self.head, self.author, self.signature)

    def __repr__(self):
        return """
        letter: {}, period: {},
        head: {},
        author: {},
        signature: {}
        """.format(self.letter, self.period, self.head, self.author, self.signature)
   
    def check_signature(self):
        letter = self.letter 
        period = self.period
        author = self.author 
        head = self.head 

        m = hashlib.sha256()
        m.update(letter)
        m.update(author)
        m.update(head)
        m.update(bin(period).encode())

        return (self.signature == m.digest())      


###     pour les tests  ###

exemple1 = Letter(b"a", 0, b"""123456789""", b"""cafe""")
exemple2 = Letter(b"b", 0, exemple1.signature, b"""456""")
exemple3 = Letter(b"b", 0, exemple1.signature, b"""456""")

if __name__ == "__main__":  
    print(exemple1.check_signature())
    exemple1.period = 5
    print(exemple1.check_signature())
