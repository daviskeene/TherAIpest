#Function to turn a string from first person into second person
import random
import nltk
from nltk import tokenize
import re
import enchant

def f2s(line):
    rep = {"'":"","I ": "you ", "am ": "are ", "my": "your",
           "we ": "they", " us": "you ","Because": "",
           "because": ""," me ": " you ","im":"you're","I'm":"you're",
           "and":"","but":"","for":"","if":"","or":"","when":"","My":"your"}

    #Replace substrings in line with those in rep
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))

    b = pattern.sub(lambda m: rep[re.escape(m.group(0))], line)
    b = random.choice(tokenize.sent_tokenize(b))

    #Split the sentence if it has a comma or because
    if "," in b:
        split = b.split("because")
        split = b.split(",")

        #Spell check
        pwl = enchant.request_pwl_dict("mywords.txt")
        d2 = enchant.DictWithPWL("en_US","mywords.txt")
        #If there is a comma, choose the side with the most amount of words to pass to the chat function.
        len_choice = max(split,key=len)
        #Replace the first space if there is a comma.
        if len_choice[:0] == "":
            len_choice = len_choice.replace(" ","",1)
        print d2.check(b)
        print len_choice

        return len_choice.lower()
    else:
        # Spell check
        pwl = enchant.request_pwl_dict("mywords.txt")
        d2 = enchant.DictWithPWL("en_US", "mywords.txt")
        # If there is a comma, choose the side with the most amount of words to pass to the chat function.
        return b.lower()

