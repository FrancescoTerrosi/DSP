from hilltools import *

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

def find_key(pt, ct, m): #pt,ct shall be list of indexes
    pairs = []
    for i in range(0,len(pt),m):
        pairs.append((create_indexes(pt[i:i+m]),create_indexes(ct[i:i+m]))) #pairs will be a list of pairs (plaintext,ciphertext)
    if len(pairs) < m:
        raise Exception("Too few pairs of plaintext ciphertext")
    k = 0 # counter for number of shift
    while k < len(pairs):
        pstar = []
        cstar = []
        for i in range(0,m):
            pstar.append(pairs[i][0]) #P* is a m x m matrix in which each line is known plaintext
            cstar.append(pairs[i][1]) #C* is a m x m matrix in which cstar[i] = ciphertext(plaintext[i])
        try:
            key = dot_product(numpy.transpose(cstar),modMatInv(numpy.transpose(pstar),len(gamma))) #da dispense
            print("!!FOUND THE KEY!!")
            return key
        except:
            shiftLeft(pairs) #provo a vedere che chiave riesco a ottenere shiftando a sinistra il vettore delle coppie, aggiornando quindi P* e C*
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
if __name__ == '__main__':
    txt = clean("scrivo un messaggio molto lungo affinche si possano ottenere numerose coppie di testo in chiaro testo cifrato da poter utilizzare per inferire la chiave di cifratura per il cifrario di Hill che e un tipo di cifrario vulnerabile ad attacchi di tipo known plaintext ossia tutti quegli attacchi in cui l'attaccante e a conoscenza di un numero arbitrario di coppie testo in chiaro testo cifrato e se uno ci pensa bene non e neanche una situazione tanto strana o difficile da ottenere infatti alcuni messaggi possono essere conosciuti a priori perche risposte a protocolli noti come ad esempio arp nelle reti locali")
    txt = clean("scrivo un messaggio abbastanza lungo affinche si possano ottenere un buon numero di coppie ma non troppe")
    key = [ [1,2,3]
           ,[3,1,1]
           ,[1,2,4] ]
    ciphertext = encrypt(txt,key)
    print("Input text: "+txt)
    print("Ciphertext: "+ciphertext)
    decrypted = decrypt(ciphertext,key)
    print("Decrypted: "+decrypt(ciphertext,key))
    print("*********** ATTACKING HILL CIPHER ***********")
    guessed_key = find_key(txt,ciphertext,len(key))
    if guessed_key is not None:
        print("Decryption of ciphertext using the guessed key:" + key2str(guessed_key))
        print(decrypt(ciphertext,guessed_key))

