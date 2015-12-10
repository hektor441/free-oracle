import free_groups as fg
from random import choice, random

# An oracle must guess identity words of n symbols

symbols = list(fg.generators.keys())
max_power = max(fg.generators.values())
powers = [i for i in range(1, max_power+1)]

# weight =: [symbol weight] [power weight]
# add_symbol : choose_symbol(symbol_weight) * choose_power(power_weight)


def weighted_choice(elements, weights):
    stock = []
    for i in range(0, len(elements)):
        element = elements[i]
        weight  = weights[i]
        
        stock += [element] * int((0.5 + weight) * 100)
    
    return choice(stock)
    

class FreeOracle:
    def __init__(self, w, n):
        self.w = w
        self.n = n
        
        self.last_fit = 0
        
        self.words   = []
        self.powers  = []
        self.weights = []
        self.populate(self.w, self.n)
    
    def populate(self, new_words, new_weights):
        # words   = [W_1,  W_2,  ... , W_w]
        # powers  = [ [W_1_powers: [letter_1_power, letter_2_power, ..., letter_n_power]]]
        # weights = [ [W_1_weightset: ([next_symbol_weights_1] [next_symbol_power_weights_1]), ...] ]
        for i in range(0, new_words):
            self.weights.append([])
            self.powers.append([])
            self.words.append("")
        for i in range(0, len(self.weights)):
            weightset = self.weights[i]
            
            symbol_weights = []
            power_weights  = []
            
            for j in range(0, new_weights):
                # next symbol weights
                symbol_weights = ([random() for symbol in symbols])
                # next symbol's power weights
                power_weights = ([random() for power in powers])
                weight = [symbol_weights, power_weights]
                weightset.append(weight)
        
        #print("Debug 1", len(self.weights[0]))   
            
    def next_letter(self):
        for i in range(0, self.w):
            weightset = self.weights[i]
            #print(len(weightset), len(self.words[i]), self.w, self.n)
            weigths   = weightset[len(self.words[i])]
            
            symbol_weights = weigths[0]
            power_weights  = weigths[1]

            next_symbol = weighted_choice(symbols, symbol_weights)
            next_power  = weighted_choice(powers, power_weights)

            self.words[i] += next_symbol
            self.powers[i].append(next_power)
    
    def generate_words(self):
        for i in range(0, self.n):
            #print("Debug 2", i)
            self.next_letter()
    
    def fit(self):
        total = 0
        for i in range(0, len(self.words)):
            sample = self.words[i]

            word = ""
            for j in range(0, len(sample)):
                word += sample[j] * self.powers[i][j]
            
            word = fg.word_simplify(word)
            if word == "e": 
                if fg.word_is_primitive(word):
                    total+= 200
                else:
                    total+= 100
            else:
                total+= len(word)
        self.last_fit = total
        return total
    
    def next_gen(self):
        self.words  = []
        self.powers = []
        
        for i in range(0, len(self.weights)):
            weightset = self.weights[i]
            for j in range(0, len(weightset)):
                weight = weightset[j]
                
                for s in range(0, len(weight[0])):
                    weight[0][s] = (weight[0][s] + random()) % 1
                                
                for t in range(0, len(weight[1])):
                    weight[1][t] = (weight[1][t] + random()) % 1
        
        #if random() > 0.75:
            # strong mutation 
        #    if random() > 0.50:
                # one more word
        #        self.w += 1
        #    else:
                # or one more letter for each word
        #        self.n += 1
                
        self.populate(self.w, self.n)