import sys
import string
import matplotlib.pyplot as plt
import math


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


def frequencies(filename, q):
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


def coincidence_indexes(frequencies_array):
    coincidence_index = 0
    count = 0
    for n in frequencies_array:
        count += n
    for i in range(0, len(frequencies_array)):
        coincidence_index += frequencies_array[i]*(frequencies_array[i]-1)
    coincidence_index /= (count*(count-1))
    return coincidence_index


def q_grams_distribution(filename, q):
    freq = frequencies(filename, q)
    temp = freq[1]
    result = []
    for i in range(0, len(temp)):
        result.append(float(temp[i])/float(freq[2]))
    return freq[0], result


def plot_frequencies(q_grams, freqs):
	d = dict()
	for i in range(0, len(q_grams)):
		d[q_grams[i]] = freqs[i]
	keys = list(d.keys())
	keys.sort()
	values = []
	for k in keys:
		values.append(d[k])
	plt.bar(keys, values, color = 'b')
	plt.title("frequencies")
	plt.show()


def fi(letter, text):
	c = 0
	for i in range(0, len(text)):
		if text[i] == letter:
			c = c+1
	return c


def entropy(q_grams):
	result = dict()
	for q in q_grams:
		h = 0
		for c in q:
			fa = float(fi(c,q))
			h = h + (fa/float(len(q)))*math.log2(fa/float(len(q)))
		result[str(q)] = -h
	return result


def plotEntropy(entropDict):
	grams = list(entropDict.keys())
	freqss = []
	for k in grams:
		freqss.append(entropDict[k])


file = sys.argv[1]
q_g = sys.argv[2]

freq_array = frequencies(file, q_g)
ci = coincidence_indexes(freq_array[1])
qgrams = q_grams_distribution(file, q_g)
print(qgrams[0])
print(qgrams[1])
entrop = entropy(qgrams[0])
plot_frequencies(grams, freqss)

