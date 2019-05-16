import sys
import FrequenciesExercise as fr

# eseguendo il comando "python3 ExerciseMain.py" vengono calcolate e stampate su console le distribuzioni empiriche degli m-grammi 
# e gli indici di coincidenze e l'entropia per m = 1,2,3,4. Al termine dell'esecuzione viene mostrato il plot delle frequenze
# delle lettere del primo capitolo di moby dick

file = "mobydick"


print("*************\t m = 1\t*************")       # Esegue i punti 1 - 2 - 3 dell'esercizio per m = 1
freq_array = fr.occurences(file, 1)
ci = fr.coincidence_indexes(freq_array[1])
print("COINCIDENCE INDEX: {}".format(ci))
print("\n")
toPrint = fr.q_grams_distribution(file, 1)
print("1-grams distribution: {}".format(toPrint))
print("\n")
entrop = fr.entropy(toPrint)
print("ENTROPY: {}".format(entrop))
print("\n")

# Commentare questa parte se si vuole omettere m = 2,3,4 che causa output verbosi #####################################

for m in range(2,5):                    # Esegue i punti 2 - 3 (non è richiesto di plottare) dell'esercizio per m = 2, 3, 4

    print("*************\t m = {}\t*************".format(m))
    freq_array = fr.occurences(file, m)
    ci = fr.coincidence_indexes(freq_array[1])
    print("COINCIDENCE INDEX: {}".format(ci))
    qgrams = fr.q_grams_distribution(file, m)
    print("\n")
    print("{}-grams: {}".format(m,qgrams))
    print("\n")
    entrop = fr.entropy(qgrams)
    print("ENTROPY: {}".format(entrop))
    print("\n")

#######################################################################################################################à

toPlotKeys = list()
for k in toPrint.keys():
    toPlotKeys.append(k)
toPlotKeys.sort()
toPlotValues = list()
for k in toPlotKeys:
    toPlotValues.append(toPrint[k])

fr.plot_frequencies(toPlotKeys,toPlotValues)

