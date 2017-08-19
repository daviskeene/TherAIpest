import numpy as np
import pandas as pd
import nltk
from nltk import tokenize
from nltk.tokenize import word_tokenize
import random
import os
import f2s

#Temporary
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
questions = ["Yes, you can always","Yes, go ahead. Tell me about"]
memory_resp = ["Earlier you mentioned,","You had previously said that"]

#Memory, for recalling past conversation topics.

mem = []
with open(r'log.txt') as memory:
    mem.extend(memory)
    #Won't store more than five responses at a time.
    if mem.__len__() == 5:
        file = open(r'log.txt', 'w')
        file.write("" + '\n')
        file.close()

#The sentiment function for the chat bot.
def chat(line):

#Tokenize the words in training_data, then use that to train.
    wordlist = set(word.lower() for statement in train for word in word_tokenize(statement[0]))

    x = [({word: (word in word_tokenize(x[0])) for word in wordlist}, x[1]) for x in train]

    classifier = nltk.NaiveBayesClassifier.train(x)

#Use the user input as testing data
    test_data = line
    if line.__len__() > 1:

            # If there is a string, return if string is labeled as positive or negative
            test_data_features = {word.lower(): (word in word_tokenize(test_data.lower())) for word in wordlist}
            sentiment = (classifier.classify(test_data_features))

#If sentiment is positive, re-write ssentence in second person and return it as a question.
            if sentiment == "pos":
                b = f2s.f2s(line)
                a = random.choice(positive)
                #If there are multiple sentences, randomly choose one.
                c = random.choice(tokenize.sent_tokenize(b))
                response = a +" "+ c + "?"
                print response
#If sentiment is negative, include some witty respionses.
            elif sentiment == "neg":
                if "gay" in line:
                    print "Look, it's 2017. You're allowed to be a homosexual if you wish. What else is bothering you?"
                if "kill myself" in line:
                    print "I'm sorry that you are feeling suicidal. Can you tell me more about why you feel this way?"
                b = f2s.f2s(line)
                a = random.choice(negative)
                c = random.choice(tokenize.sent_tokenize(b))
                print a +" "+ c
    else:
        print "No conversation engaged."
#Write user responses to the log.
    file = open(r'log.txt', 'a')
    file.write(line+'\n')
    file.close()


while True:
    chat(input())