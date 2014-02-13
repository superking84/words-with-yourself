import random
import string

languages = {'english': [letter for letter in string.uppercase]}

class Alphabet(object):
    def __init__(self, language):
        self.language = language
        self.letters = [letter for letter in languages[language]]