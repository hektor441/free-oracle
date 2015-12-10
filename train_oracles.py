from free_groups import add_generator, word_simplify

add_generator("S", 2)
add_generator("U", 3)

from free_oracles import *


N_ORACLES = 10
N_WORDS   = 5
N_LETTERS = 20
N_GENERATIONS = 10

oracles = []

for i in range(0, N_ORACLES):
    oracles.append(FreeOracle(N_WORDS, N_LETTERS))
    
for i in range(0, N_GENERATIONS):
    print("#"*10, "Generation", i, "#"*10)
    
    fits = []
    
    for j in range(0, len(oracles)):
        oracle = oracles[j]
        oracle.generate_words()
        fit = oracle.fit()
        print("Oracle",j)
        for word in oracle.words:
            print("\t", word, word_simplify(word))
        print("\t\t", fit, "\t", "*" * fit)
        fits.append(fit)
    
    median = sum(fits) / len(fits)
    print(median)
    
    # prune the below average oracles
    for oracle in oracles:
        if oracle.last_fit < median:
            oracles.remove(oracle)
        
    # update the remaining oracles
    for oracle in oracles:
        oracle.next_gen()
        
    for i in range(len(oracles), N_ORACLES):
        chosen = weighted_choice(oracles, fits)
        oracles.append(chosen)
        fits.append(chosen.fit())


