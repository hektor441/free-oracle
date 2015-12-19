# Every oracle tries to guess a word in the free group  
# fitness is calculated as follows, given a word of n letters that reduces to a word of m letters
#   the fitness of the oracle foretelling it is n / m (double if the word is primitive)
# ex. in <S, U | SS = UUU = id>  an oracle telling UUUS = S has fitness = 4 letters / 2 resulting symbols (id * S) = 2
# SSUUS = UUS has fitness 5 / 3 < 2,  SSUUU = id has fitness 5 / 1 = 5
# a primitive identity word doubles the fitness SUUUS = id has fitness 10

import free_groups as fg
from random import choice, randint, seed, random

symbols = list(fg.generators.keys())

N_GENES = 200

# an oracle is a list of seeds
#  

def new_oracle(n_letters):
    oracle = []
    n_symbols = len(symbols)
    
    for i in range(0, n_letters):
        oracle.append(randint(0, N_GENES))
        
    return oracle

def fitness(oracle, debug=False):
    word = tell_word(oracle)
    
    for i in range(0, len(oracle)):
        seed(oracle[i])
        word += choice(symbols)
        
    if debug:
        print("Oracle:"+"-".join(map(str,oracle)))
        print(word, end=" ")
    
    fit = len(word)
    word = fg.word_simplify(word)
    if word != "e":
        fit /= len(word) + 1
    else: fit*= 2 
     
    if fg.word_is_primitive(word):
        return 2 * fit
        print("*", end="")

    if debug:
        print(word)
        print("\t", fit)

    return fit

def breed(oracle, other=None):
    new_oracle = oracle[:]
    
    if other == None: other = oracle
    
    for i in range(0, len(oracle)):
        if random() > 0.4:
            new_oracle[i] = (new_oracle[i] + other[i % len(other)]) % N_GENES
        elif random() > 0.5:
            new_oracle[i] = randint(0, N_GENES)
    
    #if random() > 0.80:
    #    new_oracle.append(new_oracle[-1])
    #elif random() > 0.80:
    #    new_oracle.pop()
    
    return new_oracle

def tell_word(oracle):
    word = ""
    
    for i in range(0, len(oracle)):
        seed(oracle[i])
        word += choice(symbols)
    return word    
    
