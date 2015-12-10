from free_groups import add_generator, word_simplify

add_generator("S", 2)
add_generator("U", 3)

from free_oracles import *


N_ORACLES = 100
N_WORDS   = 10
N_LETTERS = 20
N_GENERATIONS = 100

oracles = []

for i in range(0, N_ORACLES):
    oracles.append(FreeOracle(N_WORDS, N_LETTERS))
    
for i in range(0, N_GENERATIONS):
    print("#"*10, "Generation", i, "#"*10)
    
    best  = 0
    best_oracle = None
    worst = 0
    
    for j in range(0, len(oracles)):
        oracle = oracles[j]
        oracle.generate_words()
        print("Oracle",j)
        fit = oracle.fit()
        
        if fit > best:
            best = fit
            best_oracle = oracle
        if fit < worst or worst == 0: worst = fit
    
    median = (best - worst)/2
    print("best:",best, "worst:",worst, "median:",median)
    
    for oracle in oracles:
        if oracle.last_fit < median:
            oracles.remove(oracle)
    
    print(N_ORACLES - len(oracles), "oracles pruned")        
    
    for i in range(len(oracles), N_ORACLES):
        oracles.append(best_oracle.clone())
        
    #input()