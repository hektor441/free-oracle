
generators = {}

def add_generator(letter, period):
    generators[letter] = period

def clear_generators():
    global generators
    generators = {}

def word_simplify(word):
    for letter, period in generators.items():
        if (letter * period) in word:
            word = word.replace(letter * period, "")
            word = word_simplify(word)
        
    if word == "":
        return "e"
    return word

def word_is_primitive(word):
    for i in range(0, len(word)):
        if word_simplify(word[:i]) == "e":
            return False
    return True

def unit_test():
    add_generator("S", 2)
    add_generator("U", 3)
    print("Words equal to the unity (* primitives)")
    for word in ["SSSS", "UUUSS", "SSUUU", "SSSSSS",
                 "UUUUUU", "UUUSSSS", "SSSSUUU",
                 "SSSSUUU", "SUUUSSS", "SSUUSSU"]:
        print(word,"\t", word_simplify(word), not word_is_primitive(word))
    
    for word in ["SS", "UUU", "UUSSU", "USSUU",
                 "SUUUS", "UUSSSSU", "USSSSUU",
                 "SUUSSUS", "SUSSUUS", "USSUSSU"]:
        print("* "+word,"\t", word_simplify(word), word_is_primitive(word))
    
    print("Words equal to SUS")
    for word in ["SSSSSUS", "UUUSUSSS", "SSSUSUUU",
                 "SSSSSSSUS", "UUUSUSUUU", "UUUSUSSSSS",
                "SSSSUUUSUS", "SUSSSSSUUU", "SUSSUUUSSS",
                "SSSUSUUSSU"]:
        print(word,"\t", word_simplify(word), not word_is_primitive(word))
    clear_generators()
