from free_groups import add_generator, word_simplify

add_generator("S", 2)
add_generator("U", 3)

from free_oracles import *

oracle = new_oracle(5)

print(fitness(oracle))

print("\n***")

g = breed(oracle)

print(fit(g))