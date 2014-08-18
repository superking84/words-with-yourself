import os
import string

class Wordlist(object):
    def __init__(self):
        self.all_words = []
        self.directory = {}
        src_directory = os.curdir + os.sep + "src"
        for filename in os.listdir(src_directory):
            file_location = src_directory + os.sep + filename
            self.all_words.extend([word for word in open(file_location).read().split('\n')[:-1]])
        
        for letter in string.lowercase:
            self.directory[letter] = [word for word in self.all_words if word.startswith(letter)]
        
        # implement the below to remove undesirable words from the list (racial slurs, etc.)
        # generic swear words ("fuck") are fine / will be made optional
        # self.filter('profanity')
        
    def word_check(self, tiles, rule=len):
        '''
        Check a list of letters against the wordlist for valid words.
        Counting down from maxwordlength, the function returns the best match
        based on the rule entered into the function.
        '''
        letters = [tile.letter.lower() for tile in tiles]
        candidates = []
        for i in range(len(letters)):
            maxwordlength = min(10,len(letters[i:]))
            for j in range(maxwordlength, 2, -1):
                candidate = str(''.join(letters[i:i+j]))
                if candidate in self.directory[candidate[0]]:
                    candidates.append(candidate)
                    
        if len(candidates) == 0:
            return None
        elif len(candidates) == 1:
            return candidates[0]
        else:
            # best word currently based on length;
            # the return statement below will allow
            # that to be adjusted as necessary
            return max(candidates, key=rule)