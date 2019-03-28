import sys
import FrequenciesExercise as fr

# eseguendo il comando "python3 ExerciseMain.py" vengono calcolate e stampate su console le distribuzioni empiriche degli m-grammi 
# e gli indici di coincidenze e l'entropia per m = 1,2,3,4. Al termine dell'esecuzione viene mostrato il plot delle frequenze
# delle lettere del primo capitolo di moby dick

file = "mobydick"


print("*************\t m = 1\t*************")
freq_array = fr.frequencies(file, 1)
ci = fr.coincidence_indexes(freq_array[1])
print("COINCIDENCE INDEX: {}".format(ci))
print("\n")
toPrint = fr.q_grams_distribution(file, 1)
print("1-grams: {}".format(toPrint[0]))
print("1-grams distribution: {}".format(toPrint[1]))
print("\n")
entrop = fr.entropy(toPrint[0])
print("ENTROPY: {}".format(entrop))
print("\n")

for m in range(2,5):
    print("*************\t m = {}\t*************".format(m))
    freq_array = fr.frequencies(file, m)
    ci = fr.coincidence_indexes(freq_array[1])
    print("COINCIDENCE INDEX: {}".format(ci))
    qgrams = fr.q_grams_distribution(file, m)
    print("\n")
    print("{}-grams: {}".format(m,qgrams[0]))
    print("{}-grams distribution: {}".format(m,qgrams[1]))
    print("\n")
    entrop = fr.entropy(qgrams[0])
    print("ENTROPY: {}".format(entrop))
    print("\n")

fr.plot_frequencies(toPrint[0],freq_array[1])

