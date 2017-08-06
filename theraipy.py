import nltk
from nltk.tokenize import word_tokenize
import pandas as pd
import numpy as np
import random

#Import the data from a csv file

csvdata = pd.read_csv('training_data.csv', skipinitialspace=True,delimiter=",")

#Convert data into a numpy array
csvdata1 = np.array(csvdata)
train = []

#Put contents of numpy array into empty list
train.extend(csvdata1)

#Process the user input by tokenizing it
def process(line):

    wordlist = set(word.lower() for statement in train for word in word_tokenize(statement[0]))

    x = [({word: (word in word_tokenize(x[0])) for word in wordlist}, x[1]) for x in train]

    classifier = nltk.NaiveBayesClassifier.train(x)

    test_data = line
    if line.__len__() > 1:

#If there is a string, return if string is labeled as positive or negative
        test_data_features = {word.lower(): (word in word_tokenize(test_data.lower())) for word in wordlist}

        print line
        print(classifier.classify(test_data_features))
        return(classifier.classify(test_data_features))
    else:
        print "lol"

def elaborate(extension):

    return 0

#Testing purposes, select random choice from list and predict

process(random.choice(csvdata1[:,0]))
