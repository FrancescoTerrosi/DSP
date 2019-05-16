import sys
import string


alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
         'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def __read_from_file__(filename):
    f = open(filename, "r+")
    text = ""
    for line in f:
        line = line.replace(" ", "")
        line = line.replace("\n", "")
        line = line.translate(str.maketrans('', '', string.punctuation))
        line = line.lower()
        text += line
    return text


def __read_language_frequencies__(filename):
    f = open(filename, "r+")
    d = dict()
    for line in f:
        line = line.replace("\n", "")
        line = line.split(",")
        d[line[0]] = float(line[1])/100.0
    return d


def build_matrix(text, m):
    result = []
    for i in range(0, len(text), m):
        temp = text[i:i+m]
        result.append(temp)
    return result


def super_build_matrix(filename, m):
    text = __read_from_file__(filename)
    matrix = build_matrix(text, m)
    return matrix


def build_vector(matrix, k):
    temp = []
    for row in matrix:
        temp.append(row[k])
    result = list()
    for ch in alpha:
        result.append(freq2(temp, ch))
    return result


def freq2(row, ch):
    c = 0
    for letter in row:
        if letter == ch:
            c = c + 1
    return float(c)/float(len(row))


def dot_product(v1, v2):
    result = 0
    for i in range(0, len(v1)):
        result = result + v1[i]*v2[i]
    return result


def shift(v):
    result = list()
    result.append(v[-1])
    for i in range(0, len(v)-1):
        result.append(v[i])
    return result


def compute_mg(matrix, m):
    key = []
    Mg = []
    for k in range(0, m):
        v1 = build_vector(matrix, k)
        d = __read_language_frequencies__("eng_frequencies")
        v2 = []
        for a in alpha:
            v2.append(d[a])
        m_max = 0
        temp_k = -1
        for i in range(0, len(alpha)):
            x = dot_product(v1, v2)
            if x > m_max:
                temp_k = i
                m_max = x
            v2 = shift(v2)
        Mg.append(m_max)
        key.append(alpha[temp_k])
    return Mg, ''.join(key)


def indexof(letter):
    for i in range(0, len(alpha)):
        if alpha[i] == letter:
            return i
    return -1


def extend_key(key, size):
    extkey = key
    i = 0
    while len(extkey) <= size:
        extkey = extkey + key[i%len(key)]
        i = i + 1
    return extkey


def frequencies(text, q):
    q_grams = []
    frequencies_array = []
    count = 0
    q = int(q)
    for i in range(0, len(text)-q):
        q_gram = text[i: i+q]
        if q_gram not in q_grams:
            q_grams.append(q_gram)
            for j in range(0, len(text)):
                if text[j:j+q] == q_gram:
                    count += 1
            frequencies_array.append(count)
            count = 0
    return q_grams, frequencies_array, len(text)


def coincidence_indexes(frequencies_array):
    coincidence_index = 0
    count = 0
    for n in frequencies_array:
        count += n
    for i in range(0, len(frequencies_array)):
        coincidence_index += frequencies_array[i]*(frequencies_array[i]-1)
    coincidence_index /= (count*(count-1))
    return coincidence_index

def decipher(message, key):
    size = len(message)
    extkey = extend_key(key, size)
    plaintext = ''
    for i in range(0, size):
        m_i = indexof(message[i])
        k_i = indexof(extkey[i])
        sum_mod = (m_i - k_i) % len(alpha)
        plaintext = plaintext + alpha[sum_mod]
    return plaintext


def compute_coincidence_indexes(matrix):
    for j in range(0, len(matrix[0])):
        c = []
        for i in range(0, len(matrix)):
            c.append(matrix[i][j])
        freq = frequencies(''.join(c), 1)
        print(c)
        c_i = coincidence_indexes(freq[1])
        print(c_i)



matrix = super_build_matrix(sys.argv[1], 8)
print(matrix)
compute_coincidence_indexes(matrix)
r = compute_mg(matrix, 8)
print(r[0])
print(r[1])
print(decipher(__read_from_file__("es23"), r[1]))



