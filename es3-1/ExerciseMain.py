import sys
import FrequenciesExercise as fr
from threading import Thread

file = "mobydick"

freq_array = fr.frequencies(file, 1)
ci = fr.coincidence_indexes(freq_array[1])
toPrint = fr.q_grams_distribution(file, 1)
print(toPrint[0])
print(toPrint[1])
entrop = fr.entropy(toPrint[0])
print(entrop)

for m in range(2,5):
	freq_array = fr.frequencies(file, m)
	ci = fr.coincidence_indexes(freq_array[1])
	qgrams = fr.q_grams_distribution(file, m)
	print(qgrams[0])
	print(qgrams[1])
	entrop = fr.entropy(qgrams[0])
	print(entrop)

#fr.plot_frequencies(toPrint[0],toPrint[1])

