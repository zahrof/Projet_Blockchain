import hashlib
import copy
import ed25519

class Letter(object):
    def __init__(self, letter, period, head, author):
        self._privateKey, pubK = ed25519.create_keypair()

        self.letter = letter
        self.period = period
        self.author = pubK.to_bytes()
        self.head = head

        self._m = hashlib.sha256()
        self._m.update(letter)
        self._m.update(self.author)
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
        m = hashlib.sha256()
        m.update(self.letter)
        m.update(self.author)
        m.update(self.head)
        m.update(bin(self.period).encode())

        return (self.signature == m.digest())

    def serialize(self):
        return "Letter({},{},{},{})".format(self.letter, self.period, self.head, self.author)


###     pour les tests  ###

lexemple1 = Letter(b"a", 0, b"""123456789""", b"""cafe""")
lexemple2 = Letter(b"b", 0, lexemple1.signature, b"""456""")
lexemple3 = Letter(b"b", 0, lexemple1.signature, b"""456""")

if __name__ == "__main__":  
    print(lexemple1.check_signature())
    lexemple1.period = 5
    print(lexemple1.check_signature())
    print(lexemple1.serialize())
