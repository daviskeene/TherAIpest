import random
import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk import tokenize
import re
import enchant
import os


#Create two seperate lists, one that if filled with positive responses,
#and one that is filled with negative responses. Based on the sentiment, the chatbot
#python file will select and return a random selection from these two lists.

csvdata = pd.read_csv('/home/davis/PycharmProjects/TherAIpest/training_data.csv', skipinitialspace=True,delimiter=",")

#Convert data into a numpy array
csvdata1 = np.array(csvdata)
train = []

#Put contents of numpy array into empty list
train.extend(csvdata1)

#Two lists of different responses to user input. Randomizing the response creates a conversational feel.
positive = ["How wonderful! I'm glad that","Oh, cool. Tell me more about why","Neat. Why"]
negative = ["Oh, I'm really sorry you feel that way. Can you tell me more about why","Aw, I'm sorry that","Why do you think"]

#Function to turn a string from first person into second person
def f2s(line):
    rep = {"'":"","I": "you", "am ": "are ", "my": "your", "we ": "they", " us": "you","Because": "","because": "did"," me ": " you "}
    rep = dict((re.escape(k), v) for k, v in rep.iteritems())
    pattern = re.compile("|".join(rep.keys()))
    b = pattern.sub(lambda m: rep[re.escape(m.group(0))], line)
    b = b.replace("youm","you're")
    b = random.choice(tokenize.sent_tokenize(b))
    if "," in b:
        re.sub(r'.*you','you',b)
    pwl = enchant.request_pwl_dict("mywords.txt")
    d2 = enchant.DictWithPWL("en_US","mywords.txt")
    print d2.check(b)
    return b


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
                response = a +" "+ c
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
    file = open(r'/home/davis/PycharmProjects/TherAIpest/log.txt', 'w')
    file.write('\n'+line+'\n')
    file.close()


while True:
    chat(input())