from numpy import log2
from random import randint
from englishtexts import *

rndDistrib = {}
for char in gamma:
    rndDistrib[char] = 1.0/26.0

engDistrib = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,\
              'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,\
              'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,\
              'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,\
              'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974,\
              'z': 0.00074}
                                  
shift = lambda s,n : s[n:] + s[:n]

__exp__ = lambda a,b : pow(2,a*b)

def __init__():
    englishTexts = [e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,\
                        e11,e12,e13,e14,e15,e16,e17,e18,e19,e20,\
                        e21,e22,e23,e24,e25,e26,e27,e28,e29,e30,\
                        e31,e32,e33,e34,e35,e36,e37,e38,e39,e40,\
                        e41,e42,e43,e44,e45,e46,e47,e48,e49,e50]
    randomTexts  = []
    for i in range(0,50):
        randomTexts.append(rndText())
    return englishTexts,randomTexts

def countChars(text):
    occ = {}
    for char in gamma:
        occ[char] = text.count(char)
    tot = sum(occ.values())
    for char in occ:
        occ[char] = occ[char] / tot
    return occ,-len(occ.keys())


def klDiv(p, q):
    div = 0
    for char in p:
        if char in q:
            ratio = p[char] / q[char]
            div += p[char] * log2(ratio)
        else:
            return None
    return div

def countShift(occ, i):
    s = shift(list(occ.values()),i)
    sOcc = {}
    k = 0
    for char in gamma:
        sOcc[char] = occ[gamma[k]]
        k = k + 1
    return sOcc
    


def hTest(text):
    engRes, engResQP = [], []
    rndRes, rndResQP = [], []
    occ,mlen = countChars(text)
    for i in range(0, 26):
        sOcc = countShift(occ, i)
        eDiv = klDiv(engDistrib, sOcc)
        engRes.append(abs(eDiv))
        rDiv = klDiv(rndDistrib, sOcc)
        rndRes.append(abs(rDiv))
        eResQP = klDiv(sOcc, engDistrib)
        engResQP.append(abs(eResQP))
        rResQP = klDiv(sOcc, rndDistrib)
        rndResQP.append(abs(rResQP))
    res = []
    if min(rndRes) < min(engRes):
        res.append(False)
        res.append(__exp__(mlen, min(rndResQP)))
        res.append(min(rndRes))
    else:
        res.append(True)
        res.append(__exp__(mlen, min(engResQP)))
        res.append(min(engRes))
    res.append(__exp__(mlen, res[1]))
    return res

def rndText():
    length = randint(2048,4096)
    text = ''
    for i in range(0,length):
        text = text + gamma[randint(0,len(gamma)-1)]
    return text

if __name__ == '__main__':
    englishTexts,randomTexts = __init__()
    en,ran = 0,0
    for text in englishTexts:
        a = hTest(text)
        print("Test on english text: {}".format(a))
        if a[0]:
            en = en + 1
    for text in randomTexts:
        a = hTest(text)
        print("Test on random text: {}".format(a))
        if not a[0]:
            ran = ran + 1
    print("Total times null hypotesis not rejected: {}".format(en))
    print("Total times null hypotesis rejected: {}".format(ran))

