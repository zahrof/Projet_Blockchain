def read_dict(str):
    f = open(str) # peut lever une Exception
    lst = [l for l in f.readlines()]
    f.close()
    return lst


f1 = read_dict("../dict/dict_100000_5_15.txt")
print(len(f1))