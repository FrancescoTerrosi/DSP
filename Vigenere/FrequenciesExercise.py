import sys
import string


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
    return q_grams, frequencies_array


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
        result.append(float(temp[i])/float(len(temp)))
    return freq[0], result


file = sys.argv[1]
q_g = sys.argv[2]

# freq_array = frequencies(file, q_g)
# print(coincidence_indexes(freq_array[1]))

# print(q_grams_distribution(file, q_g))
