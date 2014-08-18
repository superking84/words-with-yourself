import os
import random, string
import xlrd

languages = {'english': [letter for letter in string.uppercase]}

class Alphabet(object):
    def __init__(self, language='english'):
        self.language = language
        self.letters = [letter for letter in languages[language]]
        self.weighted = self.get_weighted_alphabet(language)
        self.letter_count = [self.weighted.count(letter) for letter in set(self.weighted)]
        
    def get_weighted_alphabet(self, language):
        letters_with_frequencies = {}
        src = os.curdir + os.sep + 'letterfiles' + os.sep + language + '.xlsx'
        worksheet = xlrd.open_workbook(src).sheet_by_index(0)
        letters = worksheet.col(0)
        frequencies = worksheet.col(1)
        for i in range(1,27):
            letters_with_frequencies[letters[i].value] = int(frequencies[i].value)
            
        output = []
        for letter in letters_with_frequencies:
            for j in range(letters_with_frequencies[letter]):
                output.append(letter.upper())
                
        return output
        
    def get_base_word_score(self, word):
        '''
        Using the particular Alphabet's letter frequency histogram, return
        a base numerical score for a particular word. Score will be based on
        letter frequency and word length. Any other calculations (bonuses
        for specific words) will be handled elsewhere. This is only for the
        word's base score.
        '''
        pass
        
if __name__ == '__main__':
    ab=Alphabet('english')
    print len(ab.weighted)