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
        
        self.words   = ["" for i in range(0, self.w)]
        self.powers  = [[] for i in range(0, self.w)]
        self.weights = []
        self.populate_weights(self.w, self.n)

    def populate_weights(self, n_words, n_letters):
        for i in range(0, n_words):
            self.weights.append([])
        
        for i in range(0, n_words):
            # weightset = weights[i]
            for j in range(0, n_letters):
                # weight = [symbol_weight, power_weight]
                symbol_weight = [random() for x in range(0, len(symbols))]
                power_weight  = [random() for x in range(0, len(powers))]
                self.weights[i].append([symbol_weight, power_weight])
    
    def generate_words(self):
        self.words   = ["" for i in range(0, self.w)]
        self.powers  = [[] for i in range(0, self.w)]
        for i in range(0, self.w):
            # weightset = weights[i]
            # powerset  = powers[i]
            for j in range(0, self.n):
                self.words[i] += weighted_choice(symbols, self.weights[i][j][0])
                self.powers[i].append(weighted_choice(powers, self.weights[i][j][1]))

    def fit(self):
        total = 0
        for i in range(0, self.w):
            sample = self.words[i]
            word = ""
            for j in range(0, len(sample)):
                word += sample[j] * self.powers[i][j]
            
            word = fg.word_simplify(word)
            #print("\t", sample, "--", word, end="\t\t")
            if word == "e":
                if fg.word_is_primitive(word):
                    total+= len(sample) * 4 + 200
                    print(len(sample), "x 4")
                else:
                    total+= len(sample) * 2 + 100
                    print(len(sample), "x 2")
            else:
                total+= len(word)
                #print(len(word))
        #print("\tfit:",total, "(",total//self.w,")")
        total //= self.w
        
        self.last_fit = total
        return total
    
    def next_gen(self):
        
        for i in range(0, self.w):
            for j in range(0, self.n):
                for s in range(0, len(symbols)):
                    self.weights[i][j][0][s] = (self.weights[i][j][0][s] + choice([0.1, 0.0, -0.1])) % 1
                    
                for t in range(0, len(powers)):
                    self.weights[i][j][1][t] = (self.weights[i][j][1][t] + choice([0.1, 0.0, -0.1])) % 1            
        
        if random() > 0.75:
            # strong mutation 
            if random() > 0.50:
                # one more word
                self.w += 1
                
                # add another set of weights for the new word
                self.weights.append([])
                
                for j in range(0, self.n):
                    symbol_weight = [random() for x in range(0, len(symbols))]
                    power_weight  = [random() for x in range(0, len(powers))]
                    self.weights[-1].append([symbol_weight, power_weight])
            else:
                # or one more letter for each word
                self.n += 1
                
                # add a new weight to each weightset
                for i in range(0, self.w):
                    symbol_weight = [random() for x in range(0, len(symbols))]
                    power_weight  = [random() for x in range(0, len(powers))]
                    self.weights[i].append([symbol_weight, power_weight])

    def clone(self):
        oracle = FreeOracle(self.w, self.n)
        oracle.last_fit = self.last_fit
        oracle.weights = self.weights
        return oracle    
    