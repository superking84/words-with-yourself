import os
from main import word_check as wc
from wordlist import Wordlist
test = [l for l in 'spunkbass']
wl=Wordlist(os.getcwd()+"\\src")

if __name__ == "__main__":
    ans = wc(test, wl)
    print ans + " is the choice!"