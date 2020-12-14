import hashlib
import ed25519

class Letter(object):
    def __init__(self, letter, period, head, author, signature = None, pkey = None):
        
        self.letter = letter
        self.period = period
        self.author = author
        self.head = head

        self._m = hashlib.sha256()
        self._m.update(letter)
        self._m.update(self.author)
        self._m.update(head)
        self._m.update(bin(period).encode())
        if signature is not None:
            self.signature = signature
            return

        self.signature = self._m.digest()
        if pkey is not None:
            self.signature = pkey.sign(self.signature, encoding='hex')
        

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
        tempS = m.digest()
        pubK = ed25519.VerifyingKey(self.author)
        try:
            pubK.verify(self.signature, tempS, encoding='hex')
            return True
        except:
            print("false")
            return False

    def serialize(self):
        return "Letter({},{},{},{},signature = {})".format(self.letter, self.period, self.head, self.author, self.signature)


###     pour les tests  ###

lexemple1 = Letter(b"a", 0, b"""123456789""", b"""cafe""")
lexemple2 = Letter(b"b", 0, lexemple1.signature, b"""456""")
lexemple3 = Letter(b"b", 0, lexemple1.signature, b"""456""")

if __name__ == "__main__":  
    print(lexemple1.check_signature())
    lexemple1.period = 5
    print(lexemple1.check_signature())
    print(lexemple1.serialize())
