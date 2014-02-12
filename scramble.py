import random
from itertools import permutations as perm

class Scrambler(object):
    def __init__(self, word):
        self.word = word
        self.perms = [item for item in perm(word, len(word))]
        
    def get_scrambled_word(self):
        return ''.join(random.choice(self.perms))