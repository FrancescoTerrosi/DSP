import sys
from Hilltools import *

# Scorrere in fondo al programma per leggerne il funzionamento passo passo

def create_indexes(block):
    indexes = []
    for ch in block:
        indexes.append(indexof(ch))
    return indexes


def create_characters(ciphervalues):
    chars = []
    for val in ciphervalues:
        chars.append(gamma[int(val)])
    return ''.join(chars)


def cipher_block(plainblock, key):
    blockvalues = create_indexes(plainblock)
    ciphervalues = dot_product(key, blockvalues)
    cipherblock = create_characters(ciphervalues)
    return cipherblock


def encrypt(text, key):
    text = clean(text)
    m = len(key)
    blocks = []
    cipherblocks = []
    for i in range(0,len(text),m):
        blocks.append(text[i:i+m])
    if len(blocks[-1])!= m:
        for i in range(len(blocks[-1]),m):
            blocks[-1] = blocks[-1] + 'a'
    for block in blocks:
        cipherblocks.append(cipher_block(block,key))
    return ''.join(cipherblocks)


def decrypt(text, key):
    key = modMatInv(key, len(gamma))
    return encrypt(text,key)


def shiftLeft(v):
    temp = v[0]
    for i in range(0,len(v)-1):
        v[i] = v[i+1]
    v[-1] = temp


def find_key(pt, ct, m): # pt e ct sono liste di indici. Questa funzione prova a rompere il cifrario di Hill
    pairs = []
    for i in range(0,len(pt),m):
        pairs.append((create_indexes(pt[i:i+m]),create_indexes(ct[i:i+m])))
    if len(pairs) < m:
        raise Exception("Non ci sono abbastanza coppie plaintext-ciphertext")
    k = 0
    while k < len(pairs):
        pstar = []
        cstar = []
        for i in range(0,m):
            pstar.append(pairs[i][0]) # P* è una matrice m x m dove ogni riga è il known plaintext
            cstar.append(pairs[i][1]) # C* è una matrice m x m dove cstar[i] = ciphertext(plaintext[i])
        try:
            key = dot_product(numpy.transpose(cstar),modMatInv(numpy.transpose(pstar),len(gamma))) # applico la formula
            print("!!FOUND THE KEY!!")
            return key
        except:
            shiftLeft(pairs) # Provo a vedere che chiave riesco a ottenere shiftando a sinistra il vettore delle coppie, aggiornando quindi P* e C*
            k = k + 1
    return None

def key2str(key):
    k2s = []
    for row in key:
        k2srow = ''
        for val in row:
            k2srow = k2srow + str(val) + ' '
        k2s.append(k2srow)
    return str(k2s).replace(",","\r\n").replace("[","\r\n").replace("]","")


##################################################################################################################

mainKey = [ [1,2,3]
           ,[3,1,1]
           ,[1,2,4] ]


# Il programma riceve come input da riga di comando il nome del file da cui leggere il testo da cifrare


f = open(sys.argv[1])
txt = ""
for line in f.readlines():
    txt += line
txt = clean(txt)

# E' possibile definire chiavi differenti ridefinendo "mainKey"
key = mainKey

# Dimostrazione del funzionamento del cifrario di Hill
ciphertext = encrypt(txt,key)
print("Input text: "+txt)
print("Ciphertext: "+ciphertext)
decrypted = decrypt(ciphertext,key)
print("Decrypted: "+decrypt(ciphertext,key))


# Avendo a disposizione coppie di plaintext - ciphertext proviamo a ricavare la chiave che abbiamo utilizzato a partire dai <pt,ct> appena calcolati

print("*********** ATTACKING HILL CIPHER ***********")
guessed_key = find_key(txt,ciphertext,len(key))
if guessed_key is not None:
   print("Decryption of ciphertext using the guessed key:" + key2str(guessed_key))
   print(decrypt(ciphertext,guessed_key))

