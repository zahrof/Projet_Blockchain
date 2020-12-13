class Blockchain(list):

    def __str__(self):
        return ", ".join([e.getStr() for e in self])