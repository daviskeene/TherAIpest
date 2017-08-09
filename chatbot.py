import random
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk import tokenize
import re
import enchant
import os


os.chdir('/home/davis/PycharmProjects/TherAIpest')

#Create two seperate lists, one that if filled with positive responses,
#and one that is filled with negative responses. Based on the sentiment, the chatbot
#python file will select and return a random selection from these two lists.

csvdata = pd.read_csv(r'training_data.csv', skipinitialspace=True,delimiter=",")

#Convert data into a numpy array
csvdata1 = np.array(csvdata)
train = []

#Put contents of numpy array into empty list
train.extend(csvdata1)

#Two lists of different responses to user input. Randomizing the response creates a conversational feel.
positive = ["How wonderful! I'm glad that","Oh, cool. Tell me more about why","Neat. Why"]
negative = ["Oh, I'm really sorry you feel that way. Can you tell me more about why","Aw, I'm sorry that","Why do you think"]

#Need to add more lists, including those for questions, adivce, etc.

#Memory, for recalling past conversation topics.

mem = []
with open(r'log.txt') as memory:
    mem.extend(memory)
    #Won't store more than five responses at a time.
    if mem.__len__() == 5:
        file = open(r'log.txt', 'w')
        file.write("" + '\n')
        file.close()

#Function to turn a string from first person into second person
def f2s(line):
    rep = {"'":"","I ": "you ", "am ": "are ", "my": "your",
           "we ": "they", " us": "you ","Because": "",
           "because": ""," me ": " you ","im":"you're","I'm":"you're",
           "and":"","but":"","for":"","if":"","or":"","when":""}

    #Replace substrings in line with those in rep
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))

    b = pattern.sub(lambda m: rep[re.escape(m.group(0))], line)
    b = random.choice(tokenize.sent_tokenize(b))

    #Split the sentence if it has a comma or because
    split = b.split("because")
    split = b.split(",")

    pwl = enchant.request_pwl_dict("mywords.txt")
    d2 = enchant.DictWithPWL("en_US","mywords.txt")

    len_choice = max(split,key=len)
    len_choice = len_choice.replace(" ","",1)

    print d2.check(b)
    print len_choice
    return len_choice.lower()


#The sentiment function for the chat bot.
def chat(line):

    wordlist = set(word.lower() for statement in train for word in word_tokenize(statement[0]))

    x = [({word: (word in word_tokenize(x[0])) for word in wordlist}, x[1]) for x in train]

    classifier = nltk.NaiveBayesClassifier.train(x)

    test_data = line
    if line.__len__() > 1:

            # If there is a string, return if string is labeled as positive or negative
            test_data_features = {word.lower(): (word in word_tokenize(test_data.lower())) for word in wordlist}
            sentiment = (classifier.classify(test_data_features))

            if sentiment == "pos":
                b = f2s(line)
                a = random.choice(positive)
                c = random.choice(tokenize.sent_tokenize(b))
                response = a +" "+ c + "?"
                print response
            elif sentiment == "neg":
                if "gay" in line:
                    print "Look, it's 2017. You're allowed to be a homosexual if you wish. What else is bothering you?"
                if "kill myself" in line:
                    print "I'm sorry that you are feeling suicidal. Can you tell me more about why you feel this way?"
                b = f2s(line)
                a = random.choice(negative)
                c = random.choice(tokenize.sent_tokenize(b))
                print a +" "+ c
    file = open(r'log.txt', 'a')
    file.write(line+'\n')
    file.close()


while True:
    chat(input())