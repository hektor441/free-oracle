from free_groups import add_generator, word_simplify

add_generator("S", 2)
add_generator("U", 3)

from free_oracles import *

oracle = FreeOracle(5, 5)

oracle.generate_words()
print(oracle.fit())
g = oracle.clone()
g.generate_words()
print(g.fit())