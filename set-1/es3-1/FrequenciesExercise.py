import string
import matplotlib.pyplot as plt
import math
from functools import reduce


# QUESTO FILE CONTIENE SOLO FUNZIONI DI UTILITà #


gamma = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']


def __read_from_file__(filename):
	f = open(filename, "r+")
	text = ""
	for line in f.readlines():
		line = line.replace('\n', '')
		line = line.replace('\t', '')
		for ch in line:
			if ch not in gamma:
				line = line.replace(ch, '')
		text += line
	return text


def occurences(filename, q):           # Calcola il numero di occorrenze dei q-grammi all'interno del testo
    text = __read_from_file__(filename)
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


def coincidence_indexes(frequencies_array):     # Calcolo degli indici di coincidenza
    coincidence_index = 0
    count = 0
    for n in frequencies_array:
        count += n
    for i in range(0, len(frequencies_array)):
        coincidence_index += frequencies_array[i]*(frequencies_array[i]-1)
    coincidence_index /= (count*(count-1))
    return coincidence_index


def q_grams_distribution(filename, q):      # Distribuzione empirica dei q-grammi
    freq = occurences(filename, q)
    temp = freq[1]
    result = []
    for i in range(0, len(temp)):
        result.append(float(temp[i])/float(freq[2]))
    d = dict()
    for i in range(0, len(freq[0])):
        d[freq[0][i]] = result[i]
    return d


def plot_frequencies(q_grams, freqs):       # Funzione per il plot della distribuzione delle 26 lettere dell'alfabeto inglese nel primo capitolo di moby dick
	d = dict()
	for i in range(0, len(q_grams)):
		d[q_grams[i]] = freqs[i]
	keys = list(d.keys())
	keys.sort()
	values = []
	for k in keys:
		values.append(d[k])
	plt.bar(keys, values, color = 'b')
	plt.title("english alphabet frequencies 1st chapter of MD")
	plt.show()


def entropy(d):         # Calcolo dell'entropia
    n = sum(d.values())
    entropy = reduce((lambda x, y: x + y), (map((lambda x: d[x] / n * math.log(d[x] / n)), d)))
    return (-1) * (entropy) / math.log(len(d.keys()))

